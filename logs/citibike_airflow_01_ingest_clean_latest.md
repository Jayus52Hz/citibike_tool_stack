# Airflow Citi Bike Ingest + Clean Report

Run time: 2026-06-10T14:49:07

- Raw trip CSV lines including header: 50662
- Clean trips loaded to MySQL: 50488
- Clean stations loaded to MySQL: 2411
- HDFS raw path: `/data/citibike/raw`
- HDFS processed path: `/data/citibike/processed`
- MinIO raw prefix: `citibike/raw`

## HDFS Listing

```text
drwxr-xr-x   - root supergroup          0 2026-06-10 14:48 /data/citibike/exports
drwxr-xr-x   - root supergroup          0 2026-06-10 14:48 /data/citibike/exports/stations_tsv
-rw-r--r--   3 root supergroup          0 2026-06-10 14:48 /data/citibike/exports/stations_tsv/_SUCCESS
-rw-r--r--   3 root supergroup     288895 2026-06-10 14:48 /data/citibike/exports/stations_tsv/part-00000-2f327ee6-8d9f-4184-a92f-7d913f05e2f7-c000.csv
drwxr-xr-x   - root supergroup          0 2026-06-10 14:48 /data/citibike/exports/trips_tsv
-rw-r--r--   3 root supergroup          0 2026-06-10 14:48 /data/citibike/exports/trips_tsv/_SUCCESS
-rw-r--r--   3 root supergroup    9812191 2026-06-10 14:48 /data/citibike/exports/trips_tsv/part-00000-615afdc3-8aeb-4412-bb4d-2f858adbf9f5-c000.csv
drwxr-xr-x   - root supergroup          0 2026-06-10 14:47 /data/citibike/mapreduce
drwxr-xr-x   - root supergroup          0 2026-06-10 14:48 /data/citibike/processed
drwxr-xr-x   - root supergroup          0 2026-06-10 14:48 /data/citibike/processed/stations_clean_parquet
-rw-r--r--   3 root supergroup          0 2026-06-10 14:48 /data/citibike/processed/stations_clean_parquet/_SUCCESS
-rw-r--r--   3 root supergroup     153417 2026-06-10 14:48 /data/citibike/processed/stations_clean_parquet/part-00000-78e1e723-6290-4072-9162-b2c7d39d0d67-c000.snappy.parquet
drwxr-xr-x   - root supergroup          0 2026-06-10 14:48 /data/citibike/processed/trips_clean_parquet
-rw-r--r--   3 root supergroup          0 2026-06-10 14:48 /data/citibike/processed/trips_clean_parquet/_SUCCESS
-rw-r--r--   3 root supergroup    1371760 2026-06-10 14:48 /data/citibike/processed/trips_clean_parquet/part-00000-5e5bfc90-6591-4bf4-a431-8fa1b68857af-c000.snappy.parquet
-rw-r--r--   3 root supergroup    1381352 2026-06-10 14:48 /data/citibike/processed/trips_clean_parquet/part-00001-5e5bfc90-6591-4bf4-a431-8fa1b68857af-c000.snappy.parquet
drwxr-xr-x   - root supergroup          0 2026-06-10 14:47 /data/citibike/raw
drwxr-xr-x   - root supergroup          0 2026-06-10 14:47 /data/citibike/raw/gbfs
-rw-r--r--   1 root supergroup     715391 2026-06-10 14:47 /data/citibike/raw/gbfs/station_information.json
-rw-r--r--   1 root supergroup    1033125 2026-06-10 14:47 /data/citibike/raw/gbfs/station_status.json
drwxr-xr-x   - root supergroup          0 2026-06-10 14:47 /data/citibike/raw/trips
-rw-r--r--   1 root supergroup   10547438 2026-06-10 14:47 /data/citibike/raw/trips/citibike_tripdata.csv
```