$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

$cmd = @'
set -e
{ echo "id,name,value"; echo "1,test,100"; } > /tmp/test.csv
/opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data/test
/opt/hadoop-3.2.1/bin/hdfs dfs -put -f /tmp/test.csv /data/test/test.csv
/opt/hadoop-3.2.1/bin/hdfs dfs -cat /data/test/test.csv
'@

docker @Compose exec -T namenode bash -lc $cmd
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
