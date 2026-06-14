param(
    [string]$JobId = "ALL" 
)

$ErrorActionPreference = "Continue"

# 1. Xac dinh cau truc duong dan he thong
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$MapReduceRoot = Join-Path $ProjectRoot "mapreduce"
$LogDir = Join-Path $ProjectRoot "logs"

if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$LogFileMD = Join-Path $LogDir "citibike_mapreduce_latest.md"
$RunID = Get-Date -Format "yyyyMMdd_HHmmss"
$RunTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Cau hinh
$HDFS_TRIPS = "/data/citibike/exports/trips_tsv"
$HDFS_STATIONS = "/data/citibike/exports/stations_tsv"
$STREAMING_JAR = "/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

# Dinh nghia danh sach Job (Dung Array de giu thu tu)
$jobList = @(
    @{ name="mr1_user_behavior";        input=$HDFS_TRIPS },
    @{ name="mr2_top_routes";           input=$HDFS_TRIPS },
    @{ name="mr3_hourly_trends";        input=$HDFS_TRIPS },
    @{ name="mr4_weekly_analysis";      input=$HDFS_TRIPS },
    @{ name="mr5_distance_calc";        input=$HDFS_TRIPS },
    @{ name="mr6_anomaly_detection";    input=$HDFS_TRIPS },
    @{ name="mr7_station_capacity";     input=$HDFS_STATIONS },
    @{ name="mr8_station_status_check"; input=$HDFS_STATIONS }
)

# Loc danh sach job can chay
if ($JobId -ne "ALL") {
    $jobList = $jobList | Where-Object { $_.name -eq $JobId }
    if ($jobList.Count -eq 0) { Write-Error "Khong tim thay job: $JobId"; exit 1 }
}

# Khoi tao file log neu chua ton tai
if (!(Test-Path $LogFileMD)) {
    "## Citi Bike MapReduce Execution Log" | Out-File -FilePath $LogFileMD -Encoding utf8
}

Write-Host "KICH HOAT HE THONG MAPREDUCE (Mode: $JobId)..." -ForegroundColor Cyan
docker exec -i citibike-namenode hadoop dfsadmin -safemode leave | Out-Null
$failedJobs = @()

foreach ($job in $jobList) {
    $job_name = $job.name
    $input_path = $job.input
    $hdfs_output = "/data/citibike/mapreduce/$job_name"
    
    Write-Host "--------------------------------------------------" -ForegroundColor Gray
    Write-Host "Dang xu ly: $job_name..." -ForegroundColor Yellow
    
    docker exec -i citibike-namenode hadoop fs -rm -r -f $hdfs_output | Out-Null
    
    $local_job_dir = Join-Path $MapReduceRoot $job_name
    $mapper_file = Join-Path $local_job_dir "mapper.py"
    $reducer_file = Join-Path $local_job_dir "reducer.py"
    
    docker cp $mapper_file "citibike-namenode:/tmp/mapper.py"
    if ($LASTEXITCODE -ne 0) { throw "Khong copy duoc mapper cho $job_name" }
    docker cp $reducer_file "citibike-namenode:/tmp/reducer.py"
    if ($LASTEXITCODE -ne 0) { throw "Khong copy duoc reducer cho $job_name" }
    docker exec -i citibike-namenode bash -c "sed -i 's/\r$//' /tmp/mapper.py && sed -i 's/\r$//' /tmp/reducer.py"
    if ($LASTEXITCODE -ne 0) { throw "Khong normalize duoc mapper/reducer cho $job_name" }
    
    $job_start = Get-Date
    
    # Chay Hadoop
    docker exec -i citibike-namenode hadoop jar $STREAMING_JAR `
        -files /tmp/mapper.py,/tmp/reducer.py `
        -mapper "python3 mapper.py" `
        -reducer "python3 reducer.py" `
        -input $input_path `
        -output $hdfs_output 2>&1 | Tee-Object -Variable hadoop_log
    $hadoopExitCode = $LASTEXITCODE
        
    $job_end = Get-Date
    $duration_sec = [math]::Round(($job_end - $job_start).TotalSeconds, 2)
    
    # Kiem tra ket qua
    $check_hdfs = docker exec -i citibike-namenode hadoop fs -ls $hdfs_output 2>&1
    $status = if ($hadoopExitCode -eq 0 -and $check_hdfs -match "part-") { "SUCCESS" } else { "FAILED" }
    
    $lines_counts = 0
    if ($status -eq "SUCCESS") {
        $lines_counts = docker exec -i citibike-namenode bash -c "hadoop fs -cat $hdfs_output/part-00000 2>/dev/null | wc -l"
    } else {
        $failedJobs += $job_name
    }
    
    # Kiem tra mau chu 
    if ($status -eq "SUCCESS") {
        $msgColor = "Green"
    } else {
        $msgColor = "Red"
    }
    
    # FIX LOI O DONG NAY (Them ngoac nhon {} bao quanh ten bien)
    Write-Host "Ket thuc ${job_name}: $status" -ForegroundColor $msgColor

    # Ghi log
    $logEntry = @"

### Job: $job_name
- **Status**: $status
- **Duration**: $duration_sec seconds
- **Records Output**: $lines_counts
"@
    if ($status -ne "SUCCESS") {
        $logEntry += @"
- **Hadoop Log Tail**:
````text
$($hadoop_log | Select-Object -Last 80 | Out-String)
````
"@
    }
    $logEntry | Out-File -FilePath $LogFileMD -Encoding utf8 -Append
}

if ($failedJobs.Count -gt 0) {
    Write-Error "MapReduce failed jobs: $($failedJobs -join ', ')"
    exit 1
}
