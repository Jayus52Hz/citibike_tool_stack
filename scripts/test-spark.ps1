$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

& (Join-Path $PSScriptRoot "test-hdfs.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

docker @Compose exec -T spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work/test_spark_hdfs.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

docker @Compose exec -T namenode /opt/hadoop-3.2.1/bin/hdfs dfs -ls /data/test/spark-output
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
