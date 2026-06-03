$ErrorActionPreference = "Stop"

$tests = @(
  "test-hdfs.ps1",
  "test-spark.ps1",
  "test-mysql.ps1",
  "test-kafka.ps1",
  "test-drill.ps1",
  "test-airflow.ps1",
  "test-superset.ps1",
  "test-minio.ps1",
  "test-sqoop.ps1"
)

foreach ($test in $tests) {
  Write-Output "===== Running $test ====="
  & (Join-Path $PSScriptRoot $test)
  if ($LASTEXITCODE -ne 0) {
    Write-Error "$test failed"
    exit $LASTEXITCODE
  }
}

Write-Output "All requested smoke tests completed."
