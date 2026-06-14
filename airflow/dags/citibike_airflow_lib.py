import json
import os
import shutil
import subprocess
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(os.environ.get("CITIBIKE_PROJECT_ROOT", "/opt/citibike_tool_stack"))
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
RAW_TRIPS_DIR = DATA_DIR / "raw" / "trips"
RAW_GBFS_DIR = DATA_DIR / "raw" / "gbfs"
EXTRACT_DIR = RAW_TRIPS_DIR / "extracted"
HDFS = "/opt/hadoop-3.2.1/bin/hdfs"
STREAMING_JAR = "/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

TRIP_URL = "https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip"
STATION_INFORMATION_URL = "https://gbfs.citibikenyc.com/gbfs/2.3/en/station_information.json"
STATION_STATUS_URL = "https://gbfs.citibikenyc.com/gbfs/2.3/en/station_status.json"

MYSQL_USER = os.environ.get("MYSQL_USER", "testuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "testpass")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "testdb")
MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD", "rootpass")
MINIO_ROOT_USER = os.environ.get("MINIO_ROOT_USER", "minioadmin")
MINIO_ROOT_PASSWORD = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")

REALTIME_TOPIC = "citibike.station_status"
REALTIME_IMAGE = "citibike-realtime-airflow:latest"
MINIO_CLIENT_IMAGE = "minio/mc:RELEASE.2024-07-15T17-46-06Z"

MAPREDUCE_JOBS = [
    ("mr1_user_behavior", "/data/citibike/exports/trips_tsv", "rpt_mr1_user_behavior"),
    ("mr2_top_routes", "/data/citibike/exports/trips_tsv", "rpt_mr2_top_routes"),
    ("mr3_hourly_trends", "/data/citibike/exports/trips_tsv", "rpt_mr3_hourly_trends"),
    ("mr4_weekly_analysis", "/data/citibike/exports/trips_tsv", "rpt_mr4_weekly_analysis"),
    ("mr5_distance_calc", "/data/citibike/exports/trips_tsv", "rpt_mr5_distance_calc"),
    ("mr6_anomaly_detection", "/data/citibike/exports/trips_tsv", "rpt_mr6_anomaly_detection"),
    ("mr7_station_capacity", "/data/citibike/exports/stations_tsv", "rpt_mr7_station_capacity"),
    ("mr8_station_status_check", "/data/citibike/exports/stations_tsv", "rpt_mr8_station_status_check"),
]


def run_command(command, input_text=None, check=True):
    print("$ " + " ".join(str(part) for part in command))
    result = subprocess.run(
        [str(part) for part in command],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result.stdout.strip()


def docker_exec(container, *args, input_text=None, check=True):
    return run_command(["docker", "exec", "-i", container, *args], input_text=input_text, check=check)


def docker_cp(source, target):
    run_command(["docker", "cp", str(source), target])


def mysql_exec(sql, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE):
    return docker_exec(
        "citibike-mysql",
        "mysql",
        f"-u{user}",
        f"-p{password}",
        "-D",
        database,
        input_text=sql,
    )


def mysql_query_scalar(sql):
    return docker_exec(
        "citibike-mysql",
        "mysql",
        "-N",
        f"-u{MYSQL_USER}",
        f"-p{MYSQL_PASSWORD}",
        "-D",
        MYSQL_DATABASE,
        "-e",
        sql,
    ).strip()


def ensure_dirs():
    for path in [LOG_DIR, RAW_TRIPS_DIR, RAW_GBFS_DIR, EXTRACT_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def download_file(url, output_path, overwrite=False):
    output_path = Path(output_path)
    if output_path.exists() and not overwrite:
        print(f"File exists: {output_path}")
        return str(output_path)
    print(f"Downloading {url} -> {output_path}")
    with urllib.request.urlopen(url, timeout=120) as response, output_path.open("wb") as out:
        shutil.copyfileobj(response, out)
    return str(output_path)


def get_trip_zip_path():
    return RAW_TRIPS_DIR / Path(urllib.request.urlparse(TRIP_URL).path).name


def get_trip_csv_path():
    csv_files = sorted(EXTRACT_DIR.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No trip CSV found under {EXTRACT_DIR}")
    return csv_files[0]


def download_and_extract_sources():
    ensure_dirs()
    zip_path = get_trip_zip_path()
    download_file(TRIP_URL, zip_path, overwrite=False)
    download_file(STATION_INFORMATION_URL, RAW_GBFS_DIR / "station_information.json", overwrite=True)
    download_file(STATION_STATUS_URL, RAW_GBFS_DIR / "station_status.json", overwrite=True)

    if EXTRACT_DIR.exists():
        shutil.rmtree(EXTRACT_DIR)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(EXTRACT_DIR)

    trip_csv = get_trip_csv_path()
    return {
        "trip_zip": str(zip_path),
        "trip_csv": str(trip_csv),
        "station_information": str(RAW_GBFS_DIR / "station_information.json"),
        "station_status": str(RAW_GBFS_DIR / "station_status.json"),
        "raw_trip_lines": sum(1 for _ in trip_csv.open("r", encoding="utf-8", errors="ignore")),
    }


def current_docker_network():
    for container in ["citibike-airflow-scheduler", "citibike-airflow-webserver", "citibike-airflow-init"]:
        output = run_command(
            [
                "docker",
                "inspect",
                container,
                "--format",
                "{{range $name, $_ := .NetworkSettings.Networks}}{{println $name}}{{end}}",
            ],
            check=False,
        )
        networks = [line.strip() for line in output.splitlines() if line.strip()]
        if networks:
            return networks[0]
    raise RuntimeError("Cannot detect Docker network for Airflow containers")


def reset_hdfs_and_upload_raw():
    sources = download_and_extract_sources()
    docker_exec(
        "citibike-namenode",
        "bash",
        "-lc",
        f"{HDFS} dfs -rm -r -f /data/citibike && "
        f"{HDFS} dfs -mkdir -p /data/citibike/raw/trips /data/citibike/raw/gbfs "
        f"/data/citibike/processed /data/citibike/exports /data/citibike/mapreduce",
    )
    docker_cp(sources["trip_csv"], "citibike-namenode:/tmp/citibike_tripdata.csv")
    docker_cp(sources["station_information"], "citibike-namenode:/tmp/station_information.json")
    docker_cp(sources["station_status"], "citibike-namenode:/tmp/station_status.json")
    docker_exec(
        "citibike-namenode",
        "bash",
        "-lc",
        f"{HDFS} dfs -put -f /tmp/citibike_tripdata.csv /data/citibike/raw/trips/citibike_tripdata.csv && "
        f"{HDFS} dfs -put -f /tmp/station_information.json /data/citibike/raw/gbfs/station_information.json && "
        f"{HDFS} dfs -put -f /tmp/station_status.json /data/citibike/raw/gbfs/station_status.json",
    )
    return sources


def upload_raw_to_minio():
    network = current_docker_network()
    cid = run_command(
        [
            "docker",
            "create",
            "--network",
            network,
            "--entrypoint",
            "/bin/sh",
            MINIO_CLIENT_IMAGE,
            "-lc",
            (
                f"mc alias set local http://minio:9000 {MINIO_ROOT_USER} {MINIO_ROOT_PASSWORD} && "
                "mc mb --ignore-existing local/citibike && "
                "mc rm --recursive --force local/citibike/raw || true && "
                "mc cp --recursive /raw local/citibike/"
            ),
        ]
    )
    try:
        docker_cp(DATA_DIR / "raw", f"{cid}:/raw")
        run_command(["docker", "start", "-a", cid])
    finally:
        run_command(["docker", "rm", "-f", cid], check=False)


def run_spark_cleaning():
    return docker_exec(
        "citibike-spark-master",
        "/opt/spark/bin/spark-submit",
        "--master",
        "spark://spark-master:7077",
        "/opt/spark/work/clean_citibike.py",
    )


def prepare_mysql_clean_tables():
    schema_sql = (PROJECT_ROOT / "mysql" / "init" / "02-citibike-schema.sql").read_text(encoding="utf-8")
    mysql_exec(
        schema_sql
        + "\nTRUNCATE TABLE citibike_trips_clean;\nTRUNCATE TABLE citibike_stations_clean;\n",
        user="root",
        password=MYSQL_ROOT_PASSWORD,
    )


def sqoop_export_clean_tables():
    docker_exec(
        "citibike-sqoop",
        "bash",
        "-lc",
        "/opt/sqoop/bin/sqoop export "
        "--connect 'jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false' "
        f"--username {MYSQL_USER} --password {MYSQL_PASSWORD} --driver com.mysql.cj.jdbc.Driver "
        "--table citibike_trips_clean --export-dir /data/citibike/exports/trips_tsv "
        "--input-fields-terminated-by '\\t' --num-mappers 1 "
        "--columns ride_id,rideable_type,started_at,ended_at,duration_minutes,start_station_id,start_station_name,"
        "end_station_id,end_station_name,start_lat,start_lng,end_lat,end_lng,member_casual",
    )
    docker_exec(
        "citibike-sqoop",
        "bash",
        "-lc",
        "/opt/sqoop/bin/sqoop export "
        "--connect 'jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false' "
        f"--username {MYSQL_USER} --password {MYSQL_PASSWORD} --driver com.mysql.cj.jdbc.Driver "
        "--table citibike_stations_clean --export-dir /data/citibike/exports/stations_tsv "
        "--input-fields-terminated-by '\\t' --num-mappers 1 "
        "--columns station_id,name,short_name,lat,lon,capacity,num_bikes_available,num_docks_available,"
        "is_installed,is_renting,is_returning,last_reported",
    )


def write_ingest_report(raw_trip_lines=None):
    trip_count = mysql_query_scalar("SELECT COUNT(*) FROM citibike_trips_clean;")
    station_count = mysql_query_scalar("SELECT COUNT(*) FROM citibike_stations_clean;")
    hdfs_listing = docker_exec("citibike-namenode", HDFS, "dfs", "-ls", "-R", "/data/citibike")
    report = [
        "# Airflow Citi Bike Ingest + Clean Report",
        "",
        f"Run time: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Raw trip CSV lines including header: {raw_trip_lines or 'n/a'}",
        f"- Clean trips loaded to MySQL: {trip_count}",
        f"- Clean stations loaded to MySQL: {station_count}",
        "- HDFS raw path: `/data/citibike/raw`",
        "- HDFS processed path: `/data/citibike/processed`",
        "- MinIO raw prefix: `citibike/raw`",
        "",
        "## HDFS Listing",
        "",
        "```text",
        hdfs_listing,
        "```",
    ]
    path = LOG_DIR / "citibike_airflow_01_ingest_clean_latest.md"
    path.write_text("\n".join(report), encoding="utf-8")
    return {"trips": int(trip_count), "stations": int(station_count), "report": str(path)}


def build_realtime_image():
    run_command(["docker", "build", "-t", REALTIME_IMAGE, str(PROJECT_ROOT / "docker" / "realtime")])


def run_temp_realtime_script(script_name, args, env=None):
    env = env or {}
    network = current_docker_network()
    command = ["docker", "create", "--network", network]
    for key, value in env.items():
        command.extend(["-e", f"{key}={value}"])
    command.extend([REALTIME_IMAGE, "python", f"/app/{script_name}", *args])
    cid = run_command(command)
    try:
        docker_cp(PROJECT_ROOT / "realtime" / script_name, f"{cid}:/app/{script_name}")
        run_command(["docker", "start", "-a", cid])
    finally:
        run_command(["docker", "rm", "-f", cid], check=False)


def prepare_realtime_table_and_topic():
    schema_sql = (PROJECT_ROOT / "mysql" / "init" / "02-citibike-schema.sql").read_text(encoding="utf-8")
    mysql_exec(schema_sql + "\nTRUNCATE TABLE citibike_station_status_stream;\n", user="root", password=MYSQL_ROOT_PASSWORD)
    docker_exec(
        "citibike-kafka",
        "/opt/kafka/bin/kafka-topics.sh",
        "--bootstrap-server",
        "kafka:9092",
        "--delete",
        "--if-exists",
        "--topic",
        REALTIME_TOPIC,
        check=False,
    )
    time.sleep(3)
    docker_exec(
        "citibike-kafka",
        "/opt/kafka/bin/kafka-topics.sh",
        "--bootstrap-server",
        "kafka:9092",
        "--create",
        "--if-not-exists",
        "--topic",
        REALTIME_TOPIC,
        "--partitions",
        "1",
        "--replication-factor",
        "1",
    )


def publish_realtime_messages(max_records=200):
    run_temp_realtime_script(
        "producer.py",
        ["--topic", REALTIME_TOPIC, "--max-records", str(max_records)],
        {
            "KAFKA_BOOTSTRAP_SERVERS": "kafka:9092",
            "CITIBIKE_STATION_STATUS_URL": STATION_STATUS_URL,
        },
    )


def consume_realtime_messages(max_records=200):
    group_id = f"citibike-airflow-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_temp_realtime_script(
        "consumer_mysql.py",
        [
            "--topic",
            REALTIME_TOPIC,
            "--group-id",
            group_id,
            "--offset-reset",
            "earliest",
            "--timeout-ms",
            "10000",
            "--max-messages",
            str(max_records),
        ],
        {
            "KAFKA_BOOTSTRAP_SERVERS": "kafka:9092",
            "MYSQL_HOST": "mysql",
            "MYSQL_PORT": "3306",
            "MYSQL_DATABASE": MYSQL_DATABASE,
            "MYSQL_USER": MYSQL_USER,
            "MYSQL_PASSWORD": MYSQL_PASSWORD,
        },
    )
    return group_id


def validate_realtime(group_id=None):
    count = mysql_query_scalar("SELECT COUNT(*) FROM citibike_station_status_stream;")
    if int(count) < 1:
        raise RuntimeError("Realtime workflow loaded zero rows")
    topic_description = docker_exec(
        "citibike-kafka",
        "/opt/kafka/bin/kafka-topics.sh",
        "--bootstrap-server",
        "kafka:9092",
        "--describe",
        "--topic",
        REALTIME_TOPIC,
    )
    report = [
        "# Airflow Citi Bike Realtime Report",
        "",
        f"Run time: {datetime.now().isoformat(timespec='seconds')}",
        f"- Topic: `{REALTIME_TOPIC}`",
        f"- Consumer group: `{group_id or 'n/a'}`",
        f"- Rows loaded to MySQL: {count}",
        "",
        "## Topic Description",
        "",
        "```text",
        topic_description,
        "```",
    ]
    path = LOG_DIR / "citibike_airflow_02_realtime_latest.md"
    path.write_text("\n".join(report), encoding="utf-8")
    return {"rows": int(count), "report": str(path)}


def run_mapreduce_job(job_name, input_path):
    output_path = f"/data/citibike/mapreduce/{job_name}"
    job_dir = PROJECT_ROOT / "mapreduce" / job_name
    mapper = job_dir / "mapper.py"
    reducer = job_dir / "reducer.py"
    if not mapper.exists() or not reducer.exists():
        raise FileNotFoundError(f"Missing mapper/reducer for {job_name}")

    docker_exec("citibike-namenode", "hadoop", "dfsadmin", "-safemode", "leave", check=False)
    docker_exec("citibike-namenode", "hadoop", "fs", "-rm", "-r", "-f", output_path, check=False)
    docker_cp(mapper, "citibike-namenode:/tmp/mapper.py")
    docker_cp(reducer, "citibike-namenode:/tmp/reducer.py")
    docker_exec(
        "citibike-namenode",
        "bash",
        "-lc",
        "sed -i 's/\\r$//' /tmp/mapper.py && sed -i 's/\\r$//' /tmp/reducer.py",
    )
    started = time.time()
    docker_exec(
        "citibike-namenode",
        "hadoop",
        "jar",
        STREAMING_JAR,
        "-files",
        "/tmp/mapper.py,/tmp/reducer.py",
        "-mapper",
        "python3 mapper.py",
        "-reducer",
        "python3 reducer.py",
        "-input",
        input_path,
        "-output",
        output_path,
    )
    count = docker_exec(
        "citibike-namenode",
        "bash",
        "-lc",
        f"{HDFS} dfs -cat {output_path}/part-* 2>/dev/null | wc -l",
    )
    return {
        "job": job_name,
        "output": output_path,
        "records": int(count.strip() or "0"),
        "duration_seconds": round(time.time() - started, 2),
    }


def write_mapreduce_report(results):
    report = ["# Airflow Citi Bike MapReduce Report", "", f"Run time: {datetime.now().isoformat(timespec='seconds')}", ""]
    for item in results:
        report.extend(
            [
                f"## {item['job']}",
                "",
                "- Status: SUCCESS",
                f"- Output: `{item['output']}`",
                f"- Records: {item['records']}",
                f"- Duration seconds: {item['duration_seconds']}",
                "",
            ]
        )
    path = LOG_DIR / "citibike_airflow_03_mapreduce_latest.md"
    path.write_text("\n".join(report), encoding="utf-8")
    return {"jobs": len(results), "report": str(path)}


def prepare_report_tables():
    schema_sql = (PROJECT_ROOT / "mysql" / "init" / "03-mapreduce-report-tables.sql").read_text(encoding="utf-8")
    mysql_exec(schema_sql, user="root", password=MYSQL_ROOT_PASSWORD)


def export_mapreduce_job(job_id, table):
    mysql_exec(f"TRUNCATE TABLE {table};")
    docker_exec(
        "citibike-sqoop",
        "bash",
        "-lc",
        "/opt/sqoop/bin/sqoop export "
        "--connect 'jdbc:mysql://mysql:3306/testdb?useSSL=false' "
        f"--username {MYSQL_USER} --password {MYSQL_PASSWORD} --table {table} "
        f"--export-dir /data/citibike/mapreduce/{job_id} "
        "--input-fields-terminated-by '\\t' --input-lines-terminated-by '\\n' "
        "--input-null-string '\\\\N' --input-null-non-string '\\\\N' -m 1",
    )
    return {"job": job_id, "table": table, "records": int(mysql_query_scalar(f"SELECT COUNT(*) FROM {table};") or "0")}


def write_export_report(results):
    report = ["# Airflow Citi Bike Export Report", "", f"Run time: {datetime.now().isoformat(timespec='seconds')}", ""]
    for item in results:
        report.append(f"- {item['table']}: {item['records']} rows")
    path = LOG_DIR / "citibike_airflow_04_export_reports_latest.md"
    path.write_text("\n".join(report), encoding="utf-8")
    return {"tables": len(results), "report": str(path)}
