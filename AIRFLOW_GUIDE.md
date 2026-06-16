# Airflow Pipeline Guide

Tai lieu nay mo ta phan Airflow orchestration cua du an. Airflow khong chi la health check nua; hien co 4 DAG tach rieng va trigger noi tiep.

## 1. Kien truc DAG

```text
citibike_01_ingest_clean
  -> citibike_02_realtime_kafka
  -> citibike_03_mapreduce
  -> citibike_04_export_reports
```

Ly do chia 4 DAG:

- De trigger tung phan khi demo/debug.
- Khong day toan bo pipeline vao mot task duy nhat.
- Moi DAG co report rieng trong `logs/`.

## 2. Danh sach DAG

| DAG | Chuc nang | Output / evidence |
| --- | --- | --- |
| `citibike_01_ingest_clean` | Download raw data, upload HDFS/MinIO, Spark clean, Sqoop load clean tables | `logs/citibike_airflow_01_ingest_clean_latest.md` |
| `citibike_02_realtime_kafka` | Build realtime image, reset Kafka topic/table, produce 200 messages, consume vao MySQL | `logs/citibike_airflow_02_realtime_latest.md` |
| `citibike_03_mapreduce` | Chay 8 Hadoop Streaming MapReduce jobs theo thu tu | `logs/citibike_airflow_03_mapreduce_latest.md` |
| `citibike_04_export_reports` | Tao report tables va Sqoop export ket qua MapReduce ve MySQL | `logs/citibike_airflow_04_export_reports_latest.md` |

Airflow image duoc build tu `docker/airflow/Dockerfile`. Image nay them Docker CLI de DAG co the dieu phoi cac container Hadoop, Spark, MySQL, Kafka, MinIO va Sqoop qua Docker socket.

## 3. Start Airflow

```powershell
cd "D:\Bigdata\New game\projects\citibike_tool_stack"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare-build-deps.ps1
docker compose up -d --build airflow-init airflow-webserver airflow-scheduler
```

Mo UI:

```text
http://127.0.0.1:8082
```

Login:

```text
admin / admin
```

## 4. Trigger pipeline

Trigger tu DAG dau tien:

```powershell
docker exec citibike-airflow-scheduler airflow dags trigger citibike_01_ingest_clean
```

DAG 1 se tu trigger DAG 2, DAG 2 trigger DAG 3, DAG 3 trigger DAG 4.

Neu can chay rieng tung phan:

```powershell
docker exec citibike-airflow-scheduler airflow dags trigger citibike_01_ingest_clean
docker exec citibike-airflow-scheduler airflow dags trigger citibike_02_realtime_kafka
docker exec citibike-airflow-scheduler airflow dags trigger citibike_03_mapreduce
docker exec citibike-airflow-scheduler airflow dags trigger citibike_04_export_reports
```

## 5. Kiem tra trang thai nhanh

Dung query metadata DB, nhanh hon goi Airflow CLI lien tuc:

```powershell
docker exec citibike-airflow-postgres psql -U airflow -d airflow -c "select dag_id, state, start_date, end_date from dag_run where dag_id like 'citibike_%' order by start_date desc limit 8;"
```

Kiem tra task cua run moi nhat:

```powershell
docker exec citibike-airflow-postgres psql -U airflow -d airflow -c "select dag_id, task_id, state from task_instance where dag_id like 'citibike_%' and start_date is not null order by start_date desc limit 20;"
```

Khong nen poll bang `airflow dags list-runs` lien tuc vi Airflow CLI load environment cham va in nhieu warning tu package phu.

## 6. Ket qua test gan nhat

Lan test Airflow gan nhat:

- `citibike_01_ingest_clean`: success.
- `citibike_02_realtime_kafka`: success.
- `citibike_03_mapreduce`: success.
- `citibike_04_export_reports`: success.

Counts sau khi export:

| Table | Rows |
| --- | ---: |
| `rpt_mr1_user_behavior` | 4 |
| `rpt_mr2_top_routes` | 4185 |
| `rpt_mr3_hourly_trends` | 24 |
| `rpt_mr4_weekly_analysis` | 14 |
| `rpt_mr5_distance_calc` | 4185 |
| `rpt_mr6_anomaly_detection` | 0 |
| `rpt_mr7_station_capacity` | 3 |
| `rpt_mr8_station_status_check` | 2 |

## 7. Evidence nen nop

- Screenshot Airflow UI hien 4 DAG `citibike_01_*` den `citibike_04_*`.
- Screenshot Graph/Grid cua tung DAG success.
- 4 file report trong `logs/citibike_airflow_*_latest.md`.
- Screenshot query MySQL row counts cua cac bang `rpt_mr*`.

## 8. Troubleshooting

Kiem tra DAG import:

```powershell
docker exec citibike-airflow-scheduler airflow dags list-import-errors
```

Kiem tra Docker CLI trong Airflow:

```powershell
docker exec citibike-airflow-scheduler docker version
```

Kiem tra log task Airflow:

```powershell
docker exec citibike-airflow-scheduler find /opt/airflow/logs -path "*citibike_*" -type f
```

Neu DAG 4 fail do Sqoop, xem log task `export_mr*_...` va kiem tra HDFS output:

```powershell
docker exec citibike-namenode /opt/hadoop-3.2.1/bin/hdfs dfs -ls /data/citibike/mapreduce
```

