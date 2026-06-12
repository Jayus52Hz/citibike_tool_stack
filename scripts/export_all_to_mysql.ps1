param(
    [Parameter(Mandatory=$true)]
    [string]$JobId
)

$ErrorActionPreference = "Continue"

# 1. Xác định cấu trúc đường dẫn hệ thống
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$LogDir = Join-Path $ProjectRoot "logs"
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$LogFileMD = Join-Path $LogDir "citibike_sqoop_export_latest.md"

$ReportTablesSql = Join-Path $ProjectRoot "mysql\init\03-mapreduce-report-tables.sql"

# =========================================================================
# TỰ ĐỘNG ĐỌC FILE SQL ĐỂ KHỞI TẠO BẢNG TRƯỚC
# =========================================================================
Write-Host "Dang kiem tra va thuc thi file SQL khoi tao bang..." -ForegroundColor Cyan

if (Test-Path $ReportTablesSql) {
    # Đọc nội dung file SQL từ Windows và đẩy trực tiếp vào container MySQL để chạy
    Get-Content $ReportTablesSql -Raw | docker exec -i citibike-mysql mysql -utestuser -ptestpass -D testdb
    
    if ($LASTEXITCODE -ne 0) {
        throw "Loi thuc thi file SQL khoi tao bang rpt_! Vui long kiem tra lai."
    }
    Write-Host "Khoi tao cấu trúc các bang tu file 03 thành công!" -ForegroundColor Green
} else {
    Write-Warning "Khong tim thay file SQL tai duong dan: $ReportTablesSql. Script se tiep tuc neu cac bang da co san."
}
# =========================================================================

# --- SU DUNG ARRAY (MANG) DE GIU THU TU ---
$jobs = @(
    @{ id="mr1_user_behavior";        table="rpt_mr1_user_behavior" },
    @{ id="mr2_top_routes";           table="rpt_mr2_top_routes" },
    @{ id="mr3_hourly_trends";        table="rpt_mr3_hourly_trends" },
    @{ id="mr4_weekly_analysis";      table="rpt_mr4_weekly_analysis" },
    @{ id="mr5_distance_calc";        table="rpt_mr5_distance_calc" },
    @{ id="mr6_anomaly_detection";    table="rpt_mr6_anomaly_detection" },
    @{ id="mr7_station_capacity";     table="rpt_mr7_station_capacity" },
    @{ id="mr8_station_status_check"; table="rpt_mr8_station_status_check" }
)

# Function xu ly
function Invoke-ExportJob($job) {
    $id = $job.id
    $table = $job.table
    
    Write-Host "Dang xu ly: $id -> $table" -ForegroundColor Yellow
    
    # 1. Lam sach bang (Chắc chắn đã chạy thành công vì bảng đã được tạo ở trên)
    docker exec -i citibike-mysql mysql -utestuser -ptestpass -D testdb -e "TRUNCATE TABLE $table;" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Khong truncate duoc bang $table"
    }
    
    # 2. Export
    $sqoopCmd = "/opt/sqoop/bin/sqoop export --connect 'jdbc:mysql://mysql:3306/testdb?useSSL=false' --username testuser --password testpass --table $table --export-dir /data/citibike/mapreduce/$id --input-fields-terminated-by '\t' --input-lines-terminated-by '\n' --input-null-string '\\N' --input-null-non-string '\\N' -m 1"
    docker exec -i citibike-sqoop bash -c "$sqoopCmd" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Sqoop export that bai cho $id -> $table"
    }
    
    # 3. Kiem tra va ghi log
    $count = docker exec -i citibike-mysql mysql -utestuser -ptestpass -D testdb -N -e "SELECT COUNT(*) FROM $table;"
    if ($LASTEXITCODE -ne 0 -or $null -eq $count) {
        throw "Khong doc duoc row count cua $table"
    }
    "Table: $table | Records: $($count.Trim())" | Out-File -FilePath $LogFileMD -Append -Encoding utf8
    Write-Host "Xong $table. Tong so dong: $($count.Trim())" -ForegroundColor Green
}

# --- LOGIC CHINH ---
if ($JobId -eq "ALL") {
    Write-Host "Dang chay TAT CA cac job theo thu tu..." -ForegroundColor Cyan
    foreach ($job in $jobs) {
        Invoke-ExportJob -job $job
    }
} else {
    # Tìm job theo id
    $foundJob = $jobs | Where-Object { $_.id -eq $JobId }
    if ($foundJob) {
        Invoke-ExportJob -job $foundJob
    } else {
        Write-Error "Khong tim thay Job ID: $JobId. Kiem tra lai ten!"
        exit 1
    }
}