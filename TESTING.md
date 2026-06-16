# Testing

Chay cac lenh duoi day tai `D:\Bigdata\New game\projects\citibike_tool_stack` sau khi `Copy-Item .env.example .env` va `docker compose up -d --build` hoan tat.
Nen doi 1-3 phut de cac service init xong truoc khi chay toan bo test.

## Quick Status

```powershell
docker compose ps
```

## HDFS

```powershell
.\scripts\test-hdfs.ps1
```

Lenh nay tao file CSV 1 dong, put vao HDFS tai `/data/test/test.csv`, sau do cat file.

## Spark

```powershell
.\scripts\test-spark.ps1
```

Spark doc CSV tu HDFS va ghi output vao `/data/test/spark-output`.

## MySQL

```powershell
.\scripts\test-mysql.ps1
```

Kiem tra insert/select bang `testdb.test_data`.

## Sqoop

```powershell
.\scripts\test-sqoop.ps1
```

Kiem tra import MySQL sang HDFS va export HDFS ve bang `sqoop_export_test`.

## Drill

```powershell
.\scripts\test-drill.ps1
```

Goi REST API Drill query file `/sample-data/test.csv`.

## Kafka

```powershell
.\scripts\test-kafka.ps1
```

Tao topic `tool-stack-test`, produce va consume message `hello-bigdata`.

## Airflow

```powershell
.\scripts\test-airflow.ps1
```

Chay DAG `tool_stack_health_check` bang CLI.

## Superset

```powershell
.\scripts\test-superset.ps1
```

Kiem tra HTTP health endpoint cua Superset.
Script cung tao/cap nhat database connection `MySQL testdb` va chay `superset test-db` voi URI MySQL.

## MinIO

```powershell
.\scripts\test-minio.ps1
```

Tao bucket `test-bucket`, upload va cat file `test.csv`.

## All Tests

```powershell
.\scripts\run-all-tests.ps1
```

Neu PowerShell chan script theo ExecutionPolicy:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-tests.ps1
```

