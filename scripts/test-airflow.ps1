$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

docker @Compose exec -T airflow-webserver airflow dags test tool_stack_health_check 2026-01-01
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
