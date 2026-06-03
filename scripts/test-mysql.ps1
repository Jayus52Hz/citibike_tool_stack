$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

$sql = @"
INSERT INTO test_data (id, name, value)
VALUES (1, 'test', 100)
ON DUPLICATE KEY UPDATE name = 'test', value = 100;
SELECT * FROM test_data;
"@

$sql | docker @Compose exec -T mysql mysql -utestuser -ptestpass testdb
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
