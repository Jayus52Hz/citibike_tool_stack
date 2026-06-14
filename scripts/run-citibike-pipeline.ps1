param(
  [string]$TripUrl = "https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip",
  [string]$StationInformationUrl = "https://gbfs.citibikenyc.com/gbfs/2.3/en/station_information.json",
  [string]$StationStatusUrl = "https://gbfs.citibikenyc.com/gbfs/2.3/en/station_status.json"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))
$Hdfs = "/opt/hadoop-3.2.1/bin/hdfs"
$RunId = Get-Date -Format "yyyyMMdd_HHmmss"
$LogDir = Join-Path $ProjectRoot "logs"
$RawTripsDir = Join-Path $ProjectRoot "data\raw\trips"
$RawGbfsDir = Join-Path $ProjectRoot "data\raw\gbfs"
$ExtractDir = Join-Path $RawTripsDir "extracted"
$ReportPath = Join-Path $LogDir "citibike_pipeline_latest.md"
$TranscriptPath = Join-Path $LogDir "citibike_pipeline_$RunId.log"

New-Item -ItemType Directory -Force $LogDir, $RawTripsDir, $RawGbfsDir, $ExtractDir | Out-Null
Start-Transcript -Path $TranscriptPath -Force | Out-Null

function Write-Step {
  param([string]$Message)
  $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
  Write-Output $line
}

function Invoke-Compose {
  param([string[]]$Arguments)
  docker @Compose @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "docker compose $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
  }
}

try {
  Write-Step "Starting Citi Bike end-to-end pipeline"
  Write-Step "Preparing local build dependencies"
  $depsSearchRoot = (Resolve-Path (Join-Path $ProjectRoot "..")).Path
  & (Join-Path $ProjectRoot "scripts\prepare-build-deps.ps1") -SearchRoot $depsSearchRoot
  if ($LASTEXITCODE -ne 0) {
    throw "prepare-build-deps.ps1 failed with exit code $LASTEXITCODE"
  }

  Write-Step "Ensuring Docker Compose stack is running"
  Invoke-Compose @("up", "-d", "--build")

  $zipName = Split-Path ([uri]$TripUrl).AbsolutePath -Leaf
  $zipPath = Join-Path $RawTripsDir $zipName

  if (-not (Test-Path $zipPath)) {
    Write-Step "Downloading trip data: $TripUrl"
    Invoke-WebRequest -Uri $TripUrl -OutFile $zipPath
  } else {
    Write-Step "Trip zip already exists: $zipPath"
  }

  Write-Step "Extracting trip zip"
  Remove-Item -Recurse -Force $ExtractDir -ErrorAction SilentlyContinue
  New-Item -ItemType Directory -Force $ExtractDir | Out-Null
  Expand-Archive -Path $zipPath -DestinationPath $ExtractDir -Force
  $tripCsv = Get-ChildItem -Path $ExtractDir -Recurse -Filter "*.csv" | Select-Object -First 1
  if (-not $tripCsv) {
    throw "No CSV file found after extracting $zipPath"
  }
  Write-Step "Trip CSV: $($tripCsv.FullName)"

  Write-Step "Downloading GBFS station JSON files"
  Invoke-WebRequest -Uri $StationInformationUrl -OutFile (Join-Path $RawGbfsDir "station_information.json")
  Invoke-WebRequest -Uri $StationStatusUrl -OutFile (Join-Path $RawGbfsDir "station_status.json")

  Write-Step "Preparing HDFS directories"
  Invoke-Compose @("exec", "-T", "namenode", "bash", "-lc", "$Hdfs dfs -rm -r -f /data/citibike && $Hdfs dfs -mkdir -p /data/citibike/raw/trips /data/citibike/raw/gbfs /data/citibike/processed /data/citibike/exports")

  Write-Step "Copying raw files into namenode container"
  Invoke-Compose @("cp", $tripCsv.FullName, "namenode:/tmp/citibike_tripdata.csv")
  Invoke-Compose @("cp", (Join-Path $RawGbfsDir "station_information.json"), "namenode:/tmp/station_information.json")
  Invoke-Compose @("cp", (Join-Path $RawGbfsDir "station_status.json"), "namenode:/tmp/station_status.json")

  Write-Step "Uploading raw files to HDFS"
  Invoke-Compose @("exec", "-T", "namenode", "bash", "-lc", "$Hdfs dfs -put -f /tmp/citibike_tripdata.csv /data/citibike/raw/trips/citibike_tripdata.csv && $Hdfs dfs -put -f /tmp/station_information.json /data/citibike/raw/gbfs/station_information.json && $Hdfs dfs -put -f /tmp/station_status.json /data/citibike/raw/gbfs/station_status.json")

  Write-Step "Uploading raw files to MinIO bucket local/citibike"
  $dataDir = Join-Path $ProjectRoot "data"
  $dataMount = "${dataDir}:/sample-data:ro"
  Invoke-Compose @("run", "--rm", "-v", $dataMount, "minio-client", "mc alias set local http://minio:9000 minioadmin minioadmin && mc mb --ignore-existing local/citibike && mc cp --recursive /sample-data/raw local/citibike/")

  Write-Step "Running Spark cleaning and normalization job"
  Invoke-Compose @("exec", "-T", "spark-master", "/opt/spark/bin/spark-submit", "--master", "spark://spark-master:7077", "/opt/spark/work/clean_citibike.py")

  Write-Step "Creating and truncating MySQL target tables"
  $schemaSql = Get-Content -Raw (Join-Path $ProjectRoot "mysql\init\02-citibike-schema.sql")
  $loadSql = @"
$schemaSql
TRUNCATE TABLE citibike_trips_clean;
TRUNCATE TABLE citibike_stations_clean;
"@
  $loadSql | docker @Compose exec -T mysql mysql -uroot -prootpass testdb
  if ($LASTEXITCODE -ne 0) {
    throw "MySQL schema setup failed with exit code $LASTEXITCODE"
  }

  Write-Step "Exporting cleaned trips from HDFS to MySQL with Sqoop"
  Invoke-Compose @("exec", "-T", "sqoop", "bash", "-lc", "/opt/sqoop/bin/sqoop export --connect 'jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false' --username testuser --password testpass --driver com.mysql.cj.jdbc.Driver --table citibike_trips_clean --export-dir /data/citibike/exports/trips_tsv --input-fields-terminated-by '\t' --num-mappers 1 --columns ride_id,rideable_type,started_at,ended_at,duration_minutes,start_station_id,start_station_name,end_station_id,end_station_name,start_lat,start_lng,end_lat,end_lng,member_casual")

  Write-Step "Exporting cleaned stations from HDFS to MySQL with Sqoop"
  Invoke-Compose @("exec", "-T", "sqoop", "bash", "-lc", "/opt/sqoop/bin/sqoop export --connect 'jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false' --username testuser --password testpass --driver com.mysql.cj.jdbc.Driver --table citibike_stations_clean --export-dir /data/citibike/exports/stations_tsv --input-fields-terminated-by '\t' --num-mappers 1 --columns station_id,name,short_name,lat,lon,capacity,num_bikes_available,num_docks_available,is_installed,is_renting,is_returning,last_reported")

  Write-Step "Collecting validation counts"
  $rawLineCount = (Get-Content -Path $tripCsv.FullName | Measure-Object -Line).Lines
  $tripCount = ("SELECT COUNT(*) FROM citibike_trips_clean;" | docker @Compose exec -T mysql mysql -N -utestuser -ptestpass testdb)
  $stationCount = ("SELECT COUNT(*) FROM citibike_stations_clean;" | docker @Compose exec -T mysql mysql -N -utestuser -ptestpass testdb)
  $sampleTrips = ("SELECT ride_id, started_at, ended_at, duration_minutes, start_station_name, end_station_name FROM citibike_trips_clean LIMIT 5;" | docker @Compose exec -T mysql mysql -utestuser -ptestpass testdb | Out-String)
  $hdfsListing = (docker @Compose exec -T namenode $Hdfs dfs -ls -R /data/citibike | Out-String)
  $minioListing = (docker @Compose run --rm minio-client "mc alias set local http://minio:9000 minioadmin minioadmin >/dev/null && mc ls --recursive local/citibike/raw" | Out-String)

  Write-Step "Writing pipeline report: $ReportPath"
  $reportLines = @(
    "# Citi Bike Pipeline Log",
    "",
    "Run ID: $RunId",
    "Run time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "",
    "## Sources",
    "",
    "- Trip history CSV ZIP: $TripUrl",
    "- GBFS station information: $StationInformationUrl",
    "- GBFS station status: $StationStatusUrl",
    "",
    "## Validation",
    "",
    "- Raw trip CSV lines including header: $rawLineCount",
    "- Clean trips loaded to MySQL: $tripCount",
    "- Clean stations loaded to MySQL: $stationCount",
    "",
    "## Storage",
    "",
    "- HDFS raw trips: ``/data/citibike/raw/trips/citibike_tripdata.csv``",
    "- HDFS raw GBFS: ``/data/citibike/raw/gbfs/``",
    "- HDFS processed parquet: ``/data/citibike/processed/``",
    "- HDFS Sqoop export TSV: ``/data/citibike/exports/``",
    "- MinIO raw bucket prefix: ``local/citibike/raw``",
    "- MySQL relational tables: ``citibike_trips_clean``, ``citibike_stations_clean``",
    "",
    "## Requirement Mapping",
    "",
    "- Da dang nguon du lieu: Citi Bike trip CSV va Citi Bike GBFS JSON.",
    "- Cai dat chuong trinh thu thap: ``scripts/run-citibike-pipeline.ps1``.",
    "- Lon hon 1000 records: $tripCount clean trip records loaded.",
    "- Lam sach, chuan hoa: ``spark/apps/clean_citibike.py``.",
    "- Luu tru vao DBMS: MySQL ``testdb``.",
    "- To chuc CSDL quan he: MySQL tables with primary keys.",
    "- Ket noi Hadoop System: HDFS raw/processed paths, Spark processing, Sqoop export.",
    "",
    "## HDFS Listing",
    "",
    '```text',
    $hdfsListing,
    '```',
    "",
    "## MinIO Listing",
    "",
    '```text',
    $minioListing,
    '```',
    "",
    "## MySQL Sample",
    "",
    '```text',
    $sampleTrips,
    '```',
    "",
    "## Full Command Transcript",
    "",
    "See: ``$TranscriptPath``"
  )
  $report = $reportLines -join [Environment]::NewLine
  Set-Content -Path $ReportPath -Value $report -Encoding UTF8

  Write-Step "Pipeline completed successfully"
  Write-Output "REPORT_PATH=$ReportPath"
  Write-Output "TRANSCRIPT_PATH=$TranscriptPath"
} finally {
  Stop-Transcript | Out-Null
}
