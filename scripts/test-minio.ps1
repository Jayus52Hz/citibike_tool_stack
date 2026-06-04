$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

$cmd = @'
mc alias set local http://minio:9000 minioadmin minioadmin
mc mb --ignore-existing local/test-bucket
{ echo "id,name,value"; echo "1,test,100"; } > /tmp/test.csv
mc cp /tmp/test.csv local/test-bucket/test.csv
mc ls local/test-bucket
mc cat local/test-bucket/test.csv
'@
$cmd = $cmd -replace "`r`n", "`n"

docker @Compose run --rm minio-client $cmd
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
