# Airflow Citi Bike Ingest + Clean Report

Run time: 2026-06-14T14:39:31

- Raw trip CSV lines including header: 50662
- Clean trips loaded to MySQL: 50488
- Clean stations loaded to MySQL: 2411
- HDFS raw path: `/data/citibike/raw`
- HDFS processed path: `/data/citibike/processed`
- MinIO raw prefix: `citibike/raw`

## HDFS Listing

```text
drwxr-xr-x   - root supergroup          0 2026-06-14 14:38 /data/citibike/exports
drwxr-xr-x   - root supergroup          0 2026-06-14 14:38 /data/citibike/exports/stations_tsv
-rw-r--r--   3 root supergroup          0 2026-06-14 14:38 /data/citibike/exports/stations_tsv/_SUCCESS
-rw-r--r--   3 root supergroup     288951 2026-06-14 14:38 /data/citibike/exports/stations_tsv/part-00000-e8b6284a-d287-47c0-8c3c-68be7caf0f24-c000.csv
drwxr-xr-x   - root supergroup          0 2026-06-14 14:38 /data/citibike/exports/trips_tsv
-rw-r--r--   3 root supergroup          0 2026-06-14 14:38 /data/citibike/exports/trips_tsv/_SUCCESS
-rw-r--r--   3 root supergroup    9812191 2026-06-14 14:38 /data/citibike/exports/trips_tsv/part-00000-ad1ee10a-af9a-43ab-9919-93e645b4674c-c000.csv
drwxr-xr-x   - root supergroup          0 2026-06-14 14:37 /data/citibike/mapreduce
drwxr-xr-x   - root supergroup          0 2026-06-14 14:38 /data/citibike/processed
drwxr-xr-x   - root supergroup          0 2026-06-14 14:38 /data/citibike/processed/stations_clean_parquet
-rw-r--r--   3 root supergroup          0 2026-06-14 14:38 /data/citibike/processed/stations_clean_parquet/_SUCCESS
-rw-r--r--   3 root supergroup     153454 2026-06-14 14:38 /data/citibike/processed/stations_clean_parquet/part-00000-3d1fa81d-a11b-46ec-bccd-7b472255832e-c000.snappy.parquet
drwxr-xr-x   - root supergroup          0 2026-06-14 14:38 /data/citibike/processed/trips_clean_parquet
-rw-r--r--   3 root supergroup          0 2026-06-14 14:38 /data/citibike/processed/trips_clean_parquet/_SUCCESS
-rw-r--r--   3 root supergroup    1371760 2026-06-14 14:38 /data/citibike/processed/trips_clean_parquet/part-00000-0a72cb4a-37c3-4c38-8c1e-7c794c76de6f-c000.snappy.parquet
-rw-r--r--   3 root supergroup    1381352 2026-06-14 14:38 /data/citibike/processed/trips_clean_parquet/part-00001-0a72cb4a-37c3-4c38-8c1e-7c794c76de6f-c000.snappy.parquet
drwxr-xr-x   - root supergroup          0 2026-06-14 14:37 /data/citibike/raw
drwxr-xr-x   - root supergroup          0 2026-06-14 14:37 /data/citibike/raw/gbfs
-rw-r--r--   1 root supergroup     715403 2026-06-14 14:37 /data/citibike/raw/gbfs/station_information.json
-rw-r--r--   1 root supergroup    1034016 2026-06-14 14:37 /data/citibike/raw/gbfs/station_status.json
drwxr-xr-x   - root supergroup          0 2026-06-14 14:37 /data/citibike/raw/trips
-rw-r--r--   1 root supergroup   10547438 2026-06-14 14:37 /data/citibike/raw/trips/citibike_tripdata.csv
```