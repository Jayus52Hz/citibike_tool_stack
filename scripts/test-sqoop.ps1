$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

& (Join-Path $PSScriptRoot "test-hdfs.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$mysqlSql = @"
INSERT INTO test_data (id, name, value)
VALUES (1, 'test', 100)
ON DUPLICATE KEY UPDATE name = 'test', value = 100;
TRUNCATE TABLE sqoop_export_test;
"@
$mysqlSql | docker @Compose exec -T mysql mysql -utestuser -ptestpass testdb
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

docker @Compose cp (Join-Path $ProjectRoot "scripts/test-sqoop.sh") sqoop:/tmp/test-sqoop.sh
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

docker @Compose exec -T sqoop bash /tmp/test-sqoop.sh
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

"SELECT * FROM sqoop_export_test;" | docker @Compose exec -T mysql mysql -utestuser -ptestpass testdb
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
