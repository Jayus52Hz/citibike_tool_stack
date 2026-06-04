$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Compose = @("compose", "-f", (Join-Path $ProjectRoot "docker-compose.yml"), "--env-file", (Join-Path $ProjectRoot ".env"))

$cmd = @'
set -e
/opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --delete --if-exists --topic tool-stack-test || true
sleep 3
/opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic tool-stack-test
echo "hello-bigdata" | /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server kafka:9092 --topic tool-stack-test
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic tool-stack-test --from-beginning --max-messages 1 --timeout-ms 10000
'@
$cmd = $cmd -replace "`r`n", "`n"

docker @Compose exec -T kafka bash -lc $cmd
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
