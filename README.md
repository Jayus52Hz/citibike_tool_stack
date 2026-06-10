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
| Streamlit GUI | http://localhost:8501 | none |
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

## Ung dung du lieu: Query, CRUD, sao luu/phuc hoi, truc quan hoa

Khoi dong GUI cung stack:

```powershell
docker compose up -d --build gui-app
```

Mo `http://localhost:8501`.

Ung dung Streamlit ho tro:

- Thuc thi query: trang `SQL Workbench` chay `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`, va cac lenh `INSERT`, `UPDATE`, `DELETE` sau khi xac nhan.
- CRUD: cac trang `Manage Trips` va `Manage Stations` cho phep them, xem, sua, xoa du lieu bang bang co the chinh sua.
- Sao luu/phuc hoi: trang `Backup / Restore` xuat cac bang MySQL duoc chon thanh file ZIP chua CSV va phuc hoi lai voi che do thay the tuy chon.
- Truc quan hoa: trang `MR Dashboard` co toi thieu 5 bieu do voi nhieu loai, gom bieu do cot, duong/vung, tron/donut va ban do tram xe.

## Cong viec da thuc hien

### 1. Ho tro thuc thi query va CRUD

- Da them trang `SQL Workbench` trong Streamlit GUI.
- Cho phep chay cac lenh doc du lieu: `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`.
- Cho phep chay cac lenh thay doi du lieu: `INSERT`, `UPDATE`, `DELETE` sau khi nguoi dung tick xac nhan.
- Da co trang `Manage Trips` de them, xem, sua, xoa bang `citibike_trips_clean`.
- Da co trang `Manage Stations` de them, xem, sua, xoa bang `citibike_stations_clean`.
- Da cap nhat ket noi MySQL de app chay duoc ca ngoai host va trong Docker thong qua `MYSQL_HOST`, `MYSQL_PORT`.
- Da them package `cryptography` vao `gui_app/requirements.txt` de PyMySQL ket noi duoc MySQL 8 voi co che `caching_sha2_password`.

### 2. Sao luu va phuc hoi du lieu

- Da them trang `Backup / Restore` trong Streamlit GUI.
- Chuc nang sao luu cho phep chon cac bang MySQL va tai ve file ZIP.
- File backup gom cac file CSV trong thu muc `tables/` va file `manifest.json` mo ta thoi gian tao, ten bang, so dong, danh sach cot.
- Chuc nang phuc hoi cho phep upload file ZIP backup va ghi lai du lieu vao MySQL.
- Co tuy chon xoa du lieu hien tai truoc khi phuc hoi.

### 3. Truc quan hoa du lieu

- Da co trang `Dashboard` trong Streamlit de doc cac bang report `rpt_mr*` tu MySQL.
- Dashboard ho tro 2 che do: `Bang du lieu` va `Bieu do`.
- Dashboard co toi thieu 5 bieu do va nhieu loai bieu do:
  - Bieu do cot cho hanh vi nguoi dung, top tuyen duong, phan tich theo ngay.
  - Bieu do duong/vung cho xu huong theo gio.
  - Bieu do tron/donut cho anomaly va capacity tram.
  - Ban do vi tri tram xe trong trang `Manage Stations`.
- Da them script `scripts/refresh-dashboard-reports.ps1` de nap lai cac bang report `rpt_mr*` tu du lieu sach trong MySQL.

Chay lai du lieu dashboard:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\refresh-dashboard-reports.ps1
```

### 4. Superset

- Superset da co service trong `docker-compose.yml` va chay tai `http://localhost:8089`.
- Tai khoan mac dinh: `admin` / `admin`.
- Superset init tu dong tao ket noi database `MySQL testdb`.
- Co the dung Superset de tao dashboard truc quan hoa tu cac bang:
  - `rpt_mr1_user_behavior`
  - `rpt_mr2_top_routes`
  - `rpt_mr3_hourly_trends`
  - `rpt_mr4_weekly_analysis`
  - `rpt_mr5_distance_calc`
  - `rpt_mr6_anomaly_detection`
  - `rpt_mr7_station_capacity`
  - `rpt_mr8_station_status_check`

Khoi dong Superset:

```powershell
docker compose up -d --build superset
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
