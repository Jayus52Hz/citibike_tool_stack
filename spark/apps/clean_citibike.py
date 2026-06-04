from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    coalesce,
    explode,
    from_unixtime,
    length,
    lit,
    regexp_replace,
    round,
    to_timestamp,
    trim,
    unix_timestamp,
)


HDFS_BASE = "hdfs://namenode:9000/data/citibike"


def clean_text(column):
    return regexp_replace(trim(coalesce(column.cast("string"), lit(""))), r"[\t\r\n]+", " ")


spark = (
    SparkSession.builder.appName("citibike-clean-normalize")
    .getOrCreate()
)

raw_trips_path = f"{HDFS_BASE}/raw/trips/*.csv"
raw_station_info_path = f"{HDFS_BASE}/raw/gbfs/station_information.json"
raw_station_status_path = f"{HDFS_BASE}/raw/gbfs/station_status.json"

trips_raw = spark.read.option("header", "true").csv(raw_trips_path)

trips_clean = (
    trips_raw.select(
        clean_text(col("ride_id")).alias("ride_id"),
        clean_text(col("rideable_type")).alias("rideable_type"),
        to_timestamp(col("started_at")).alias("started_at"),
        to_timestamp(col("ended_at")).alias("ended_at"),
        clean_text(col("start_station_id")).alias("start_station_id"),
        clean_text(col("start_station_name")).alias("start_station_name"),
        clean_text(col("end_station_id")).alias("end_station_id"),
        clean_text(col("end_station_name")).alias("end_station_name"),
        col("start_lat").cast("double").alias("start_lat"),
        col("start_lng").cast("double").alias("start_lng"),
        col("end_lat").cast("double").alias("end_lat"),
        col("end_lng").cast("double").alias("end_lng"),
        clean_text(col("member_casual")).alias("member_casual"),
    )
    .dropDuplicates(["ride_id"])
    .filter(length(col("ride_id")) > 0)
    .filter(col("started_at").isNotNull())
    .filter(col("ended_at").isNotNull())
    .filter(col("start_station_id") != "")
    .filter(col("end_station_id") != "")
    .filter(col("start_lat").isNotNull())
    .filter(col("start_lng").isNotNull())
    .filter(col("end_lat").isNotNull())
    .filter(col("end_lng").isNotNull())
    .withColumn(
        "duration_minutes",
        round((unix_timestamp(col("ended_at")) - unix_timestamp(col("started_at"))) / 60.0, 2),
    )
    .filter(col("duration_minutes") > 0)
    .filter(col("duration_minutes") <= 24 * 60)
)

trips_for_export = trips_clean.select(
    col("ride_id"),
    col("rideable_type"),
    col("started_at").cast("string").alias("started_at"),
    col("ended_at").cast("string").alias("ended_at"),
    col("duration_minutes").cast("string").alias("duration_minutes"),
    col("start_station_id"),
    col("start_station_name"),
    col("end_station_id"),
    col("end_station_name"),
    col("start_lat").cast("string").alias("start_lat"),
    col("start_lng").cast("string").alias("start_lng"),
    col("end_lat").cast("string").alias("end_lat"),
    col("end_lng").cast("string").alias("end_lng"),
    col("member_casual"),
)

station_info_root = spark.read.option("multiLine", "true").json(raw_station_info_path)
station_status_root = spark.read.option("multiLine", "true").json(raw_station_status_path)

station_info = station_info_root.select(explode(col("data.stations")).alias("s")).select(
    clean_text(col("s.station_id")).alias("station_id"),
    clean_text(col("s.name")).alias("name"),
    clean_text(col("s.short_name")).alias("short_name"),
    col("s.lat").cast("double").alias("lat"),
    col("s.lon").cast("double").alias("lon"),
    coalesce(col("s.capacity").cast("int"), lit(0)).alias("capacity"),
)

station_status = station_status_root.select(explode(col("data.stations")).alias("s")).select(
    clean_text(col("s.station_id")).alias("station_id"),
    coalesce(col("s.num_bikes_available").cast("int"), lit(0)).alias("num_bikes_available"),
    coalesce(col("s.num_docks_available").cast("int"), lit(0)).alias("num_docks_available"),
    coalesce(col("s.is_installed").cast("int"), lit(0)).alias("is_installed"),
    coalesce(col("s.is_renting").cast("int"), lit(0)).alias("is_renting"),
    coalesce(col("s.is_returning").cast("int"), lit(0)).alias("is_returning"),
    from_unixtime(col("s.last_reported").cast("long")).alias("last_reported"),
)

stations_clean = (
    station_info.join(station_status, "station_id", "left")
    .filter(length(col("station_id")) > 0)
    .dropDuplicates(["station_id"])
)

stations_for_export = stations_clean.select(
    col("station_id"),
    col("name"),
    col("short_name"),
    col("lat").cast("string").alias("lat"),
    col("lon").cast("string").alias("lon"),
    col("capacity").cast("string").alias("capacity"),
    coalesce(col("num_bikes_available"), lit(0)).cast("string").alias("num_bikes_available"),
    coalesce(col("num_docks_available"), lit(0)).cast("string").alias("num_docks_available"),
    coalesce(col("is_installed"), lit(0)).cast("string").alias("is_installed"),
    coalesce(col("is_renting"), lit(0)).cast("string").alias("is_renting"),
    coalesce(col("is_returning"), lit(0)).cast("string").alias("is_returning"),
    coalesce(col("last_reported"), lit("1970-01-01 00:00:00")).alias("last_reported"),
)

trips_clean.write.mode("overwrite").parquet(f"{HDFS_BASE}/processed/trips_clean_parquet")
stations_clean.write.mode("overwrite").parquet(f"{HDFS_BASE}/processed/stations_clean_parquet")

trips_for_export.coalesce(1).write.mode("overwrite").option("delimiter", "\t").csv(
    f"{HDFS_BASE}/exports/trips_tsv"
)
stations_for_export.coalesce(1).write.mode("overwrite").option("delimiter", "\t").csv(
    f"{HDFS_BASE}/exports/stations_tsv"
)

print(f"raw_trip_rows={trips_raw.count()}")
print(f"clean_trip_rows={trips_clean.count()}")
print(f"clean_station_rows={stations_clean.count()}")

spark.stop()
