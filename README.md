# Citi Bike Big Data Pipeline

Du an dung Docker Compose de chay mot pipeline Big Data end-to-end tren du lieu Citi Bike:

```text
Citi Bike raw data
  -> HDFS + MinIO
  -> Spark clean/normalize
  -> MySQL
  -> Kafka realtime
  -> Hadoop MapReduce
  -> MySQL report tables
  -> Streamlit GUI + Superset
```

## 1. Trang thai theo rubric

| Nhom viec | Trang thai | Bang chung trong project |
| --- | --- | --- |
| Docker Compose build du tools va ket noi voi nhau | Done | `docker-compose.yml`, `scripts/run-all-tests.ps1` |
| File huong dan chay | Done | `README.md`, `CITIBIKE_PIPELINE_GUIDE.md` |
| Airflow orchestration | Done | 4 DAGs trong `airflow/dags/citibike_*.py` |
| Da dang nguon du lieu | Done | Citi Bike trip CSV zip + GBFS station JSON/status |
| Chuong trinh thu thap du lieu | Done | `scripts/run-citibike-pipeline.ps1`, `realtime/producer.py` |
| Du lieu lon hon 1000 records | Done | lan test gan nhat: 50,488 trips, 2,411 stations |
| Lam sach, chuan hoa du lieu | Done | `spark/apps/clean_citibike.py` |
| Luu tru vao DBMS | Done | MySQL tables `citibike_*` |
| CSDL quan he / NoSQL | Done | MySQL relational + MinIO object storage |
| Ket noi Hadoop System | Done | HDFS, YARN, MapReduce, Sqoop export |
| Ho tro query | Done | Streamlit page `SQL Workbench` |
| Ho tro CRUD | Done | Streamlit pages `Manage Trips`, `Manage Stations` |
| Sao luu, phuc hoi du lieu | Done | Streamlit page `Backup / Restore` |
| Truc quan hoa toi thieu 5 bieu do, 3 loai | Done | Streamlit `Dashboard` + Superset |
| MapReduce | Done | 8 jobs trong `mapreduce/` |
| GUI quan ly du lieu | Done | Streamlit app tai `http://127.0.0.1:8501` |

Phan cua Nang khong bi thieu: query, CRUD, backup/restore va visualization da co trong `gui_app/pages/`. Neu can nop minh chung, chay pipeline va mo GUI de chup cac trang `SQL Workbench`, `Manage Trips`, `Manage Stations`, `Backup / Restore`, `Dashboard`.

## 2. Cau truc thu muc

```text
citibike_tool_stack/
  airflow/
    dags/
      citibike_01_ingest_clean.py     Airflow DAG: raw ingest + Spark clean + MySQL load
      citibike_02_realtime_kafka.py   Airflow DAG: GBFS -> Kafka -> MySQL realtime
      citibike_03_mapreduce.py        Airflow DAG: 8 Hadoop Streaming jobs
      citibike_04_export_reports.py   Airflow DAG: Sqoop export report tables
      citibike_airflow_lib.py         Shared helper cho Airflow DAGs
      health_check_dag.py             Airflow smoke-test DAG
  data/
    raw/
      trips/                      Citi Bike trip CSV zip va file da extract
      gbfs/                       GBFS station_information/status JSON
  docker/
    airflow/                      Airflow image co Docker CLI
    drill/                        Drill config override
    hadoop-python/                Hadoop image co Python de chay mapper/reducer
    realtime/                     Dockerfile cho Kafka producer/consumer
    sqoop/                        Sqoop Dockerfile va build deps
    superset/                     Superset Dockerfile/config
  gui_app/
    app.py                        Streamlit home
    db_config.py                  MySQL helper
    pages/
      1_*_Dashboard.py            Visualization tu bang report
      2_*_Manage_Trips.py         CRUD trips
      3_*_Manage_Stations.py      CRUD stations
      4_SQL_Workbench.py          Query + SQL CRUD co xac nhan
      5_Backup_Restore.py         Backup/restore MySQL bang ZIP/CSV
  hadoop-conf/                    Hadoop client config
  logs/                           Bao cao moi nhat sau khi chay script
  mapreduce/
    mr1_user_behavior/
    mr2_top_routes/
    mr3_hourly_trends/
    mr4_weekly_analysis/
    mr5_distance_calc/
    mr6_anomaly_detection/
    mr7_station_capacity/
    mr8_station_status_check/
  mysql/
    init/                         Schema MySQL va bang report
  realtime/
    producer.py                   GBFS -> Kafka
    consumer_mysql.py             Kafka -> MySQL
  scripts/
    prepare-build-deps.ps1        Kiem tra/copy/tai dependency cho build
    run-all-tests.ps1             Smoke test tat ca service
    run-citibike-pipeline.ps1     Batch pipeline
    run-citibike-realtime-test.ps1 Realtime validation
    run-all-jobs.ps1              Chay MapReduce jobs
    export_all_to_mysql.ps1       Export MR result ve MySQL
    refresh-dashboard-reports.ps1 Tao/lap lai report dashboard bang SQL
  spark/
    apps/
      clean_citibike.py           Spark cleaning job
  docker-compose.yml
  README.md
  CITIBIKE_PIPELINE_GUIDE.md
  AIRFLOW_GUIDE.md
  README_MAPREDUCE.md
  TESTING.md
```

## 3. Yeu cau moi truong

- Docker Desktop dang chay.
- Docker nen co toi thieu 12 GB RAM kha dung vi stack gom Hadoop, Spark, Kafka, MySQL, Airflow, Superset, Drill va MinIO.
- Chay lenh trong PowerShell.
- Thu muc lam viec:

```powershell
cd "D:\Bigdata\New game\projects\citibike_tool_stack"
```

## 4. Chay nhanh

Neu clone moi chua co `.env`:

```powershell
Copy-Item .env.example .env
```

Chuan bi dependency build va start stack:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare-build-deps.ps1
docker compose up -d --build
docker compose ps
```

Chay smoke test:

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
- Streamlit: `http://localhost:8501`

## Citi Bike Batch and Realtime Pipeline

Chay pipeline chinh:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-pipeline.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-realtime-test.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "ALL"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "ALL"
```

Hoac chay bang Airflow orchestration:

```powershell
docker compose up -d --build airflow-init airflow-webserver airflow-scheduler
docker exec citibike-airflow-scheduler airflow dags trigger citibike_01_ingest_clean
```

Airflow chia pipeline thanh 4 DAG trigger lan luot:

- `citibike_01_ingest_clean`
- `citibike_02_realtime_kafka`
- `citibike_03_mapreduce`
- `citibike_04_export_reports`

Mo GUI:

```text
http://127.0.0.1:8501
```

Huong dan chi tiet nam trong `CITIBIKE_PIPELINE_GUIDE.md`.
Huong dan rieng cho Airflow nam trong `AIRFLOW_GUIDE.md`.

## 5. Build dependency va file Hadoop zip

Khong bat buoc phai co file Hadoop zip rieng tren may de build stack nay. Hadoop chay tu Docker image `bde2020/hadoop-*`, va project da co image bo sung Python trong `docker/hadoop-python/` de chay MapReduce Python.

Thu muc `docker/sqoop/deps/` can cac file cho image Sqoop:

- `sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz`
- `mysql-connector-j-8.0.33.jar`
- `commons-lang-2.6.jar`

Script sau se xu ly tu dong:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare-build-deps.ps1
```
Neu may da co file trong workspace cha, script se copy vao `docker/sqoop/deps/`. Neu khong co, script se tai tu Apache Archive/Maven Central. Vi vay khi build moi nen chay script nay truoc `docker compose up -d --build`.

## 6. URL dich vu

| Service | URL / Port | Login |
| --- | --- | --- |
| Streamlit GUI | http://127.0.0.1:8501 | none |
| Superset | http://127.0.0.1:8089 | `admin` / `admin` |
| Hadoop NameNode | http://127.0.0.1:9870 | none |
| Hadoop ResourceManager | http://127.0.0.1:8088 | none |
| Spark Master | http://127.0.0.1:8091 | none |
| Spark Worker | http://127.0.0.1:8092 | none |
| MySQL | `127.0.0.1:3307` | `testuser` / `testpass` |
| Drill | http://127.0.0.1:8047 | none |
| Airflow | http://127.0.0.1:8082 | `admin` / `admin` |
| MinIO API | http://127.0.0.1:9002 | `minioadmin` / `minioadmin` |
| MinIO Console | http://127.0.0.1:9003 | `minioadmin` / `minioadmin` |
| Kafka | `127.0.0.1:9092` | none |

## 7. Cac bang chinh

MySQL database: `testdb`

Bang du lieu sach:

- `citibike_trips_clean`
- `citibike_stations_clean`
- `citibike_station_status_stream`

Bang report MapReduce:

- `rpt_mr1_user_behavior`
- `rpt_mr2_top_routes`
- `rpt_mr3_hourly_trends`
- `rpt_mr4_weekly_analysis`
- `rpt_mr5_distance_calc`
- `rpt_mr6_anomaly_detection`
- `rpt_mr7_station_capacity`
- `rpt_mr8_station_status_check`

## 8. Dung stack

Dung container nhung giu volume:

```powershell
docker compose down
```

Xoa ca volume du lieu:

```powershell
docker compose down -v
```

