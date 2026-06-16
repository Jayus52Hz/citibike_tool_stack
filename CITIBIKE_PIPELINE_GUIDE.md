# Citi Bike Pipeline Runbook

Tai lieu nay la checklist chuan de chay lai pipeline tu dau tren Windows PowerShell.

## 1. Chuan bi

Mo Docker Desktop truoc, sau do vao thu muc project:

```powershell
cd "D:\Bigdata\New game\projects\citibike_tool_stack"
```

Neu clone moi chua co `.env`:

```powershell
Copy-Item .env.example .env
```

Kiem tra/copy/tai dependency can cho build:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare-build-deps.ps1
```

Ghi chu:

- Khong can file `hadoop-3.3.4.tar.gz` local.
- Hadoop duoc lay tu Docker image.
- Dependency Sqoop duoc dat trong `docker/sqoop/deps/`.
- Neu dependency chua co local, script se tai tu Apache Archive/Maven Central.

## 2. Build va start stack

```powershell
docker compose up -d --build
docker compose ps
```

Lan dau co the mat nhieu phut vi Docker phai pull image va build image rieng cho Sqoop, Superset, Hadoop Python va GUI.

Doi 1-3 phut sau khi container len truoc khi chay test vi Hadoop, Drill, Airflow va Superset can thoi gian init.

## 3. Smoke test tools

Chay toan bo smoke test:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-tests.ps1
```

Expected:

- HDFS tao va doc duoc `/data/test/test.csv`.
- Spark doc HDFS va ghi output thanh cong.
- MySQL doc duoc bang test.
- Sqoop import/export duoc voi MySQL va HDFS.
- Drill query duoc sample CSV.
- Kafka produce/consume duoc message.
- Airflow DAG health check chay success.
- Superset health endpoint OK va co ket noi MySQL.
- MinIO tao bucket va object test thanh cong.

Neu fail do service chua san sang, kiem tra:

```powershell
docker compose ps
```

Sau do doi them va chay lai script test.

## 3.5. Chay pipeline bang Airflow orchestration

Neu muon demo pipeline bang Airflow, start Airflow truoc:

```powershell
docker compose up -d --build airflow-init airflow-webserver airflow-scheduler
```

Mo Airflow UI:

```text
http://127.0.0.1:8082
```

Login:

```text
admin / admin
```

Trigger DAG dau tien:

```powershell
docker exec citibike-airflow-scheduler airflow dags trigger citibike_01_ingest_clean
```

Airflow se chay 4 DAG theo thu tu:

```text
citibike_01_ingest_clean
  -> citibike_02_realtime_kafka
  -> citibike_03_mapreduce
  -> citibike_04_export_reports
```

Co the chay rieng tung DAG khi debug:

```powershell
docker exec citibike-airflow-scheduler airflow dags trigger citibike_01_ingest_clean
docker exec citibike-airflow-scheduler airflow dags trigger citibike_02_realtime_kafka
docker exec citibike-airflow-scheduler airflow dags trigger citibike_03_mapreduce
docker exec citibike-airflow-scheduler airflow dags trigger citibike_04_export_reports
```

Huong dan chi tiet: `AIRFLOW_GUIDE.md`.

## 4. Chay batch pipeline

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-pipeline.ps1
```

Pipeline nay thuc hien:

```text
Raw Citi Bike data
  -> copy raw len HDFS
  -> copy raw vao MinIO
  -> Spark clean/normalize
  -> ghi Parquet len HDFS
  -> ghi bang clean vao MySQL
```

Output chinh:

- HDFS raw: `/data/citibike/raw`
- HDFS processed: `/data/citibike/processed`
- MinIO raw: bucket/path `citibike/raw`
- MySQL table `citibike_trips_clean`
- MySQL table `citibike_stations_clean`
- Log moi nhat: `logs/citibike_pipeline_latest.md`

Lenh kiem tra nhanh MySQL:

```powershell
docker exec citibike-mysql mysql -utestuser -ptestpass testdb -e "SELECT COUNT(*) AS trips FROM citibike_trips_clean; SELECT COUNT(*) AS stations FROM citibike_stations_clean;"
```

Lan test gan nhat trong workspace nay:

- `citibike_trips_clean`: 50,488 rows
- `citibike_stations_clean`: 2,411 rows

## 5. Chay realtime Kafka

Validation mot batch realtime:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-realtime-test.ps1
```

Flow:

```text
Citi Bike GBFS station_status
  -> Kafka topic citibike.station_status
  -> MySQL table citibike_station_status_stream
```

Log moi nhat:

```text
logs/citibike_realtime_latest.md
```

Chay producer/consumer lien tuc:

```powershell
docker compose --profile realtime up -d --build realtime-producer realtime-consumer
```

Dung realtime service:

```powershell
docker compose stop realtime-producer realtime-consumer
```

## 6. Chay MapReduce

Chay tat ca 8 jobs:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "ALL"
```

Chay rieng mot job:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "mr1_user_behavior"
```

Danh sach jobs:

| Job | Noi dung |
| --- | --- |
| MR1 | User behavior theo member/casual va loai xe |
| MR2 | Top route pho bien |
| MR3 | Xu huong theo gio |
| MR4 | Phan tich theo ngay trong tuan |
| MR5 | Tinh khoang cach trung binh theo route |
| MR6 | Phat hien anomaly |
| MR7 | Phan loai station capacity |
| MR8 | Kiem tra station status |

Output HDFS:

```text
/data/citibike/mapreduce/mr1_user_behavior
/data/citibike/mapreduce/mr2_top_routes
/data/citibike/mapreduce/mr3_hourly_trends
/data/citibike/mapreduce/mr4_weekly_analysis
/data/citibike/mapreduce/mr5_distance_calc
/data/citibike/mapreduce/mr6_anomaly_detection
/data/citibike/mapreduce/mr7_station_capacity
/data/citibike/mapreduce/mr8_station_status_check
```

Log moi nhat:

```text
logs/citibike_mapreduce_latest.md
```

## 7. Export MapReduce report ve MySQL

Sau khi MapReduce thanh cong, export report tables:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "ALL"
```

Bang report tao trong MySQL:

- `rpt_mr1_user_behavior`
- `rpt_mr2_top_routes`
- `rpt_mr3_hourly_trends`
- `rpt_mr4_weekly_analysis`
- `rpt_mr5_distance_calc`
- `rpt_mr6_anomaly_detection`
- `rpt_mr7_station_capacity`
- `rpt_mr8_station_status_check`

Log moi nhat:

```text
logs/citibike_sqoop_export_latest.md
```

Kiem tra nhanh:

```powershell
docker exec citibike-mysql mysql -utestuser -ptestpass testdb -e "SHOW TABLES LIKE 'rpt_mr%';"
```

## 8. Refresh dashboard reports bang SQL

Neu chi can tao lai bang report dashboard tu MySQL clean data, khong chay lai Hadoop MapReduce:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\refresh-dashboard-reports.ps1
```

Script nay huu ich khi can demo nhanh GUI dashboard.

## 9. Mo GUI va thao tac du lieu

Mo Streamlit:

```text
http://127.0.0.1:8501
```

Neu GUI chua len:

```powershell
docker compose up -d --build gui-app
docker compose logs --tail=100 gui-app
```

Trang trong GUI:

| Trang | Chuc nang |
| --- | --- |
| Dashboard | Hien thi bang va bieu do MapReduce/report |
| Manage Trips | Them, sua, xoa, loc va xem trip clean |
| Manage Stations | Them, sua, xoa, loc va xem station clean |
| SQL Workbench | Chay `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`, va `INSERT/UPDATE/DELETE` co xac nhan |
| Backup / Restore | Tao ZIP backup CSV va restore lai MySQL |

Phan cua Nang nam o cac trang:

- `SQL Workbench`: query.
- `Manage Trips` va `Manage Stations`: CRUD.
- `Backup / Restore`: sao luu, phuc hoi.
- `Dashboard`: visualization toi thieu 5 bieu do va 3 loai chart.

## 10. Superset

Mo Superset:

```text
http://127.0.0.1:8089
```

Login:

```text
admin / admin
```

Superset co connection MySQL mac dinh:

```text
mysql+pymysql://testuser:testpass@mysql:3306/testdb
```

SQL Lab query mau:

```sql
SELECT COUNT(*) FROM citibike_trips_clean;
SELECT COUNT(*) FROM citibike_stations_clean;
SELECT COUNT(*) FROM citibike_station_status_stream;
SELECT * FROM rpt_mr1_user_behavior;
SELECT * FROM rpt_mr2_top_routes ORDER BY trip_count DESC LIMIT 10;
```

## 11. Evidence de nop

Nen nop kem cac file/log sau:

- `logs/citibike_airflow_01_ingest_clean_latest.md`
- `logs/citibike_airflow_02_realtime_latest.md`
- `logs/citibike_airflow_03_mapreduce_latest.md`
- `logs/citibike_airflow_04_export_reports_latest.md`
- `logs/citibike_pipeline_latest.md`
- `logs/citibike_realtime_latest.md`
- `logs/citibike_mapreduce_latest.md`
- `logs/citibike_sqoop_export_latest.md`
- Screenshot `docker compose ps`
- Screenshot Airflow UI 4 DAG success
- Screenshot Streamlit `Dashboard`
- Screenshot Streamlit `SQL Workbench`
- Screenshot Streamlit `Manage Trips`
- Screenshot Streamlit `Manage Stations`
- Screenshot Streamlit `Backup / Restore`
- Screenshot Superset neu dung Superset de demo chart

## 12. Dung va reset

Dung stack nhung giu volume:

```powershell
docker compose down
```

Xoa volume de chay lai tu dau:

```powershell
docker compose down -v
```

Sau khi `down -v`, can chay lai batch pipeline, realtime, MapReduce va export de co lai du lieu.

