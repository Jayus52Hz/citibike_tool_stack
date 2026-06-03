$ErrorActionPreference = "Stop"

$response = Invoke-WebRequest -Uri "http://localhost:8089/health" -UseBasicParsing
Write-Output "Superset health status: $($response.StatusCode)"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

docker @Compose exec -T superset superset set-database-uri -d "MySQL testdb" -u "mysql+pymysql://testuser:testpass@mysql:3306/testdb"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

"n" | docker @Compose exec -T superset superset test-db "mysql+pymysql://testuser:testpass@mysql:3306/testdb"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
