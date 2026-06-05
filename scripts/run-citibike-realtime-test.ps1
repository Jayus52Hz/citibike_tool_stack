$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))
$Topic = "citibike.station_status"
$MaxRecords = 200
$LogDir = Join-Path $ProjectRoot "logs"
$RunId = Get-Date -Format "yyyyMMdd_HHmmss"
$ReportPath = Join-Path $LogDir "citibike_realtime_latest.md"
$TranscriptPath = Join-Path $LogDir "citibike_realtime_$RunId.log"

New-Item -ItemType Directory -Force $LogDir | Out-Null
Start-Transcript -Path $TranscriptPath -Force | Out-Null

function Write-Step {
  param([string]$Message)
  Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
}

function Invoke-Compose {
  param([string[]]$Arguments)
  docker @Compose @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "docker compose $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
  }
}

try {
  Write-Step "Starting Citi Bike realtime Kafka validation"
  Invoke-Compose @("up", "-d", "--build", "kafka", "mysql")
  Invoke-Compose @("build", "realtime-producer", "realtime-consumer")

  Write-Step "Applying MySQL schema and truncating realtime table"
  $schemaSql = Get-Content -Raw (Join-Path $ProjectRoot "mysql\init\02-citibike-schema.sql")
  $loadSql = @"
$schemaSql
TRUNCATE TABLE citibike_station_status_stream;
"@
  $loadSql | docker @Compose exec -T mysql mysql -uroot -prootpass testdb
  if ($LASTEXITCODE -ne 0) {
    throw "MySQL schema setup failed with exit code $LASTEXITCODE"
  }

  Write-Step "Recreating Kafka topic $Topic"
  docker @Compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --delete --if-exists --topic $Topic | Out-Host
  Start-Sleep -Seconds 3
  Invoke-Compose @("exec", "-T", "kafka", "/opt/kafka/bin/kafka-topics.sh", "--bootstrap-server", "kafka:9092", "--create", "--if-not-exists", "--topic", $Topic, "--partitions", "1", "--replication-factor", "1")

  Write-Step "Publishing $MaxRecords station status messages to Kafka"
  Invoke-Compose @("run", "--rm", "realtime-producer", "python", "/app/producer.py", "--topic", $Topic, "--max-records", "$MaxRecords")

  Write-Step "Consuming Kafka messages into MySQL"
  $GroupId = "citibike-realtime-validation-$RunId"
  Invoke-Compose @("run", "--rm", "realtime-consumer", "python", "/app/consumer_mysql.py", "--topic", $Topic, "--group-id", $GroupId, "--offset-reset", "earliest", "--timeout-ms", "10000", "--max-messages", "$MaxRecords")

  Write-Step "Collecting validation counts"
  $topicDescription = (docker @Compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --describe --topic $Topic | Out-String)
  $mysqlCount = ("SELECT COUNT(*) FROM citibike_station_status_stream;" | docker @Compose exec -T mysql mysql -N -utestuser -ptestpass testdb)
  $mysqlSample = ("SELECT station_id, observed_at, num_bikes_available, num_docks_available, kafka_topic, kafka_offset FROM citibike_station_status_stream ORDER BY kafka_offset LIMIT 10;" | docker @Compose exec -T mysql mysql -utestuser -ptestpass testdb | Out-String)

  if ([int]$mysqlCount -lt 1) {
    throw "Realtime validation failed: no rows were loaded into MySQL"
  }

  $report = @(
    "# Citi Bike Realtime Kafka Log",
    "",
    "Run ID: $RunId",
    "Run time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "",
    "## Kafka",
    "",
    "- Topic: ``$Topic``",
    "- Published station status messages: $MaxRecords",
    "- Consumer group: ``$GroupId``",
    "",
    "## MySQL",
    "",
    "- Table: ``citibike_station_status_stream``",
    "- Rows loaded from Kafka: $mysqlCount",
    "",
    "## Realtime Flow",
    "",
    "GBFS station_status JSON -> ``realtime/producer.py`` -> Kafka topic ``$Topic`` -> ``realtime/consumer_mysql.py`` -> MySQL table ``citibike_station_status_stream``.",
    "",
    "## Topic Description",
    "",
    '```text',
    $topicDescription,
    '```',
    "",
    "## MySQL Sample",
    "",
    '```text',
    $mysqlSample,
    '```',
    "",
    "## Full Command Transcript",
    "",
    "See: ``$TranscriptPath``"
  ) -join [Environment]::NewLine

  Set-Content -Path $ReportPath -Value $report -Encoding UTF8
  Write-Step "Realtime validation completed successfully"
  Write-Output "REPORT_PATH=$ReportPath"
  Write-Output "TRANSCRIPT_PATH=$TranscriptPath"
} finally {
  Stop-Transcript | Out-Null
}
