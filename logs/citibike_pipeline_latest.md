# Citi Bike Pipeline Log

Run ID: 20260605_142839
Run time: 2026-06-05 14:38:12

## Sources

- Trip history CSV ZIP: https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip
- GBFS station information: https://gbfs.citibikenyc.com/gbfs/2.3/en/station_information.json
- GBFS station status: https://gbfs.citibikenyc.com/gbfs/2.3/en/station_status.json

## Validation

- Raw trip CSV lines including header: 50662
- Clean trips loaded to MySQL: 50488
- Clean stations loaded to MySQL: 2410

## Storage

- HDFS raw trips: `/data/citibike/raw/trips/citibike_tripdata.csv`
- HDFS raw GBFS: `/data/citibike/raw/gbfs/`
- HDFS processed parquet: `/data/citibike/processed/`
- HDFS Sqoop export TSV: `/data/citibike/exports/`
- MinIO raw bucket prefix: `local/citibike/raw`
- MySQL relational tables: `citibike_trips_clean`, `citibike_stations_clean`

## Requirement Mapping

- Da dang nguon du lieu: Citi Bike trip CSV va Citi Bike GBFS JSON.
- Cai dat chuong trinh thu thap: `scripts/run-citibike-pipeline.ps1`.
- Lon hon 1000 records: 50488 clean trip records loaded.
- Lam sach, chuan hoa: `spark/apps/clean_citibike.py`.
- Luu tru vao DBMS: MySQL `testdb`.
- To chuc CSDL quan he: MySQL tables with primary keys.
- Ket noi Hadoop System: HDFS raw/processed paths, Spark processing, Sqoop export.

## HDFS Listing

```text
drwxr-xr-x   - root supergroup          0 2026-06-05 07:33 /data/citibike/exports
drwxr-xr-x   - root supergroup          0 2026-06-05 07:33 /data/citibike/exports/stations_tsv
-rw-r--r--   3 root supergroup          0 2026-06-05 07:33 /data/citibike/exports/stations_tsv/_SUCCESS
-rw-r--r--   3 root supergroup     288792 2026-06-05 07:33 /data/citibike/exports/stations_tsv/part-00000-fc5df896-3283-482c-9f63-5823fbbdbfed-c000.csv
drwxr-xr-x   - root supergroup          0 2026-06-05 07:33 /data/citibike/exports/trips_tsv
-rw-r--r--   3 root supergroup          0 2026-06-05 07:33 /data/citibike/exports/trips_tsv/_SUCCESS
-rw-r--r--   3 root supergroup    9812191 2026-06-05 07:33 /data/citibike/exports/trips_tsv/part-00000-b5355c86-b983-482b-8f9c-ecebbb478238-c000.csv
drwxr-xr-x   - root supergroup          0 2026-06-05 07:33 /data/citibike/processed
drwxr-xr-x   - root supergroup          0 2026-06-05 07:33 /data/citibike/processed/stations_clean_parquet
-rw-r--r--   3 root supergroup          0 2026-06-05 07:33 /data/citibike/processed/stations_clean_parquet/_SUCCESS
-rw-r--r--   3 root supergroup     153294 2026-06-05 07:33 /data/citibike/processed/stations_clean_parquet/part-00000-28cf5139-9e62-4be2-a588-5ec0e6e8c39b-c000.snappy.parquet
drwxr-xr-x   - root supergroup          0 2026-06-05 07:33 /data/citibike/processed/trips_clean_parquet
-rw-r--r--   3 root supergroup          0 2026-06-05 07:33 /data/citibike/processed/trips_clean_parquet/_SUCCESS
-rw-r--r--   3 root supergroup    1371760 2026-06-05 07:33 /data/citibike/processed/trips_clean_parquet/part-00000-e545f1c3-8372-4901-8dc5-2c97f5c342f4-c000.snappy.parquet
-rw-r--r--   3 root supergroup    1381352 2026-06-05 07:33 /data/citibike/processed/trips_clean_parquet/part-00001-e545f1c3-8372-4901-8dc5-2c97f5c342f4-c000.snappy.parquet
drwxr-xr-x   - root supergroup          0 2026-06-05 07:30 /data/citibike/raw
drwxr-xr-x   - root supergroup          0 2026-06-05 07:31 /data/citibike/raw/gbfs
-rw-r--r--   1 root supergroup     715069 2026-06-05 07:31 /data/citibike/raw/gbfs/station_information.json
-rw-r--r--   1 root supergroup    1033641 2026-06-05 07:31 /data/citibike/raw/gbfs/station_status.json
drwxr-xr-x   - root supergroup          0 2026-06-05 07:31 /data/citibike/raw/trips
-rw-r--r--   1 root supergroup   10547438 2026-06-05 07:31 /data/citibike/raw/trips/citibike_tripdata.csv

```

## MinIO Listing

```text
[2026-06-05 07:32:13 UTC] 698KiB STANDARD gbfs/station_information.json
[2026-06-05 07:32:13 UTC]1009KiB STANDARD gbfs/station_status.json
[2026-06-05 07:32:13 UTC] 1.8MiB STANDARD trips/JC-202401-citibike-tripdata.csv.zip
[2026-06-05 07:32:14 UTC]  10MiB STANDARD trips/extracted/JC-202401-citibike-tripdata.csv
[2026-06-05 07:32:13 UTC]   562B STANDARD trips/extracted/__MACOSX/._JC-202401-citibike-tripdata.csv

```

## MySQL Sample

```text
ride_id	started_at	ended_at	duration_minutes	start_station_name	end_station_name
000053077D7822F0	2024-01-26 18:22:58	2024-01-26 18:28:24	5.43	12 St & Sinatra Dr N	South Waterfront Walkway - Sinatra Dr & 1 St
0000F3C8C29B74D7	2024-01-26 14:24:04	2024-01-26 14:31:45	7.68	Adams St & 12 St	Hoboken Terminal - River St & Hudson Pl
0001252629A4BD21	2024-01-04 08:13:46	2024-01-04 08:16:45	2.98	Brunswick St	Grove St PATH
0001B9BA3391D989	2024-01-25 12:42:10	2024-01-25 12:45:33	3.38	Warren St	City Hall
0001E9D2FB2A2FF7	2024-01-03 18:27:11	2024-01-03 18:31:59	4.8	4 St & Grand St	Grand St & 14 St

```

## Full Command Transcript

See: `D:\Bigdata\citibike_tool_stack\logs\citibike_pipeline_20260605_142839.log`
