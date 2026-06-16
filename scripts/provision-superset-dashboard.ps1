$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$ScriptPath = Join-Path $PSScriptRoot "provision_superset_dashboard.py"
$ContainerScriptPath = "/tmp/provision_superset_dashboard.py"
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

Write-Host "Starting MySQL and Superset..." -ForegroundColor Cyan
docker @Compose up -d mysql superset-init superset
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Refreshing MySQL report tables from processed data..." -ForegroundColor Cyan
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "refresh-dashboard-reports.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Copying provisioning script into Superset container..." -ForegroundColor Cyan
docker cp $ScriptPath "citibike-superset:$ContainerScriptPath"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Creating Superset datasets, charts, and dashboard..." -ForegroundColor Cyan
docker @Compose exec -T superset python $ContainerScriptPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Done. Open http://127.0.0.1:8089/superset/dashboard/citibike-mapreduce-report/ and login admin/admin." -ForegroundColor Green
