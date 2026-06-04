# Citi Bike Data Pipeline Guide

This project now includes an end-to-end pipeline for the data collection assignment.

## Run

```powershell
cd "E:\NhapMonDuLieuLon\project\citibike_tool_stack"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-pipeline.ps1
```

## Outputs

- Raw data on HDFS: `/data/citibike/raw`
- Cleaned Parquet on HDFS: `/data/citibike/processed`
- Sqoop TSV exports on HDFS: `/data/citibike/exports`
- Raw files in MinIO: `citibike/raw`
- Relational DBMS tables in MySQL `testdb`:
  - `citibike_trips_clean`
  - `citibike_stations_clean`
- Latest report: `logs/citibike_pipeline_latest.md`

## Superset

Open `http://localhost:8089` and log in with `admin` / `admin`.

Use SQL Lab with the existing MySQL connection and run:

```sql
SELECT COUNT(*) FROM citibike_trips_clean;
SELECT COUNT(*) FROM citibike_stations_clean;
SELECT * FROM citibike_trips_clean LIMIT 100;
```

Recommended charts:

- Trip count by `started_at`
- Average `duration_minutes` by `member_casual`
- Top start stations by trip count
- Bike availability by station from `citibike_stations_clean`
