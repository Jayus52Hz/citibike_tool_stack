# Citi Bike Big Data Tool Stack

Project nay chi dung de dung tool stack Big Data bang Docker Compose. Du lieu test tu sinh gom 1 dong: `1,test,100`.

## Prerequisites

- Docker Desktop dang chay.
- Toi thieu 12 GB RAM kha dung cho Docker la thuc te hon vi stack gom Hadoop, Spark, Kafka, Airflow, Superset, Drill, MySQL va MinIO.
- Chay lenh trong PowerShell tai thu muc `D:\Bigdata\New game\citibike_tool_stack`.

## Start

```powershell
cd "D:\Bigdata\New game\citibike_tool_stack"
Copy-Item .env.example .env
docker compose up -d --build
docker compose ps
```

Lan dau se mat thoi gian vi can pull images va build image Sqoop/Superset.
Sau khi container len, doi them 1-3 phut truoc khi chay smoke test vi Hadoop, Drill, Airflow va Superset can thoi gian init.

## URLs and Ports

| Service | URL / Port | Login |
| --- | --- | --- |
| Hadoop NameNode UI | http://localhost:9870 | none |
| Hadoop ResourceManager UI | http://localhost:8088 | none |
| Hadoop NodeManager UI | http://localhost:8042 | none |
| Hadoop HistoryServer UI | http://localhost:19888 | none |
| Spark Master UI | http://localhost:8091 | none |
| Spark Worker UI | http://localhost:8092 | none |
| MySQL | localhost:3307 | `testuser` / `testpass` |
| Drill UI | http://localhost:8047 | none |
| ZooKeeper | localhost:2181 | internal/Drill coordination |
| Kafka | localhost:9092 exposed, tests use internal `kafka:9092` | none |
| Airflow | http://localhost:8082 | `admin` / `admin` |
| Superset | http://localhost:8089 | `admin` / `admin` |
| MinIO API | http://localhost:9002 | `minioadmin` / `minioadmin` |
| MinIO Console | http://localhost:9003 | `minioadmin` / `minioadmin` |

## Smoke Tests

Chay tung test:

```powershell
.\scripts\test-hdfs.ps1
.\scripts\test-spark.ps1
.\scripts\test-mysql.ps1
.\scripts\test-sqoop.ps1
.\scripts\test-drill.ps1
.\scripts\test-kafka.ps1
.\scripts\test-airflow.ps1
.\scripts\test-superset.ps1
.\scripts\test-minio.ps1
```

Hoac chay tat ca:

```powershell
.\scripts\run-all-tests.ps1
```

Neu PowerShell bao `running scripts is disabled`, chay bang:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-tests.ps1
```

Neu test fail do service chua san sang, kiem tra `docker compose ps`, doi them vai chuc giay va chay lai script do.

Ket qua ky vong:

- HDFS tao `/data/test/test.csv` va `hdfs dfs -cat` in `id,name,value` va `1,test,100`.
- Spark doc `hdfs://namenode:9000/data/test/test.csv`, ghi `/data/test/spark-output`, va in `spark_rows= 1`.
- MySQL select duoc bang `test_data`.
- Sqoop import `test_data` sang HDFS va export lai vao `sqoop_export_test`.
- Drill REST query tra ve row tu `/sample-data/test.csv`.
- Kafka consume duoc message `hello-bigdata`.
- Realtime Kafka pipeline tao topic `citibike.station_status`, day station status tu GBFS vao Kafka, va consumer ghi vao MySQL bang `citibike_station_status_stream`.
- Airflow DAG `tool_stack_health_check` chay success bang `airflow dags test`.
- Superset health endpoint tra HTTP 200 va ket noi duoc MySQL `testdb`.
- MinIO bucket `test-bucket` co file `test.csv`.

## Service Hostnames

Tat ca service cung nam tren network Docker `bigdata_net`. Khi ket noi tu container khac, dung hostname service:

- HDFS: `hdfs://namenode:9000`
- YARN ResourceManager: `resourcemanager:8088`
- Spark master: `spark://spark-master:7077`
- MySQL: `mysql:3306`
- Drill: `drill:8047`
- ZooKeeper: `zookeeper:2181`
- Kafka: `kafka:9092`
- Airflow metadata DB: `airflow-postgres:5432`
- Superset: `superset:8088`
- MinIO: `http://minio:9000`

## Citi Bike Batch and Realtime Pipeline

Chay batch pipeline de tai du lieu Citi Bike, luu raw vao HDFS/MinIO, lam sach bang Spark, va export vao MySQL:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-pipeline.ps1
```

Chay realtime Kafka validation:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-realtime-test.ps1
```

Realtime flow:

```text
Citi Bike GBFS station_status -> Kafka topic citibike.station_status -> MySQL table citibike_station_status_stream
```

Chay realtime lien tuc:

```powershell
docker compose --profile realtime up -d --build realtime-producer realtime-consumer
```

## Stop and Clean

Dung stack nhung giu volume:

```powershell
docker compose down
```

Xoa ca data volume cua project:

```powershell
docker compose down -v
```

## Notes

- Superset init tu dong tao database connection `MySQL testdb`. Neu can tao lai thu cong, dung URI `mysql+pymysql://testuser:testpass@mysql:3306/testdb`.
- Drill test dang query file local mounted vao container tai `/sample-data/test.csv`. Neu muon cau hinh Drill query HDFS, tao storage plugin trong UI theo huong dan trong `manual-steps.md`.
- Sqoop 1.4.7 la tool cu; image da cai Hadoop client va MySQL JDBC driver. Neu build/download archive bi loi mang, chay lai `docker compose build sqoop`.
