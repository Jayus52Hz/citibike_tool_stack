from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from citibike_airflow_lib import (
    prepare_mysql_clean_tables,
    reset_hdfs_and_upload_raw,
    run_spark_cleaning,
    sqoop_export_clean_tables,
    upload_raw_to_minio,
    write_ingest_report,
)


@dag(
    dag_id="citibike_01_ingest_clean",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["citibike", "pipeline", "01_ingest_clean"],
)
def citibike_01_ingest_clean():
    @task
    def stage_raw_to_hdfs():
        return reset_hdfs_and_upload_raw()

    @task
    def stage_raw_to_minio():
        upload_raw_to_minio()

    @task
    def spark_clean_and_normalize():
        run_spark_cleaning()

    @task
    def load_clean_tables():
        prepare_mysql_clean_tables()
        sqoop_export_clean_tables()

    @task
    def validate_and_report(raw_sources):
        return write_ingest_report(raw_trip_lines=raw_sources.get("raw_trip_lines"))

    trigger_next = TriggerDagRunOperator(
        task_id="trigger_citibike_02_realtime_kafka",
        trigger_dag_id="citibike_02_realtime_kafka",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    raw_sources = stage_raw_to_hdfs()
    minio_done = stage_raw_to_minio()
    spark_done = spark_clean_and_normalize()
    mysql_done = load_clean_tables()
    report_done = validate_and_report(raw_sources)

    raw_sources >> minio_done >> spark_done >> mysql_done >> report_done >> trigger_next


citibike_01_ingest_clean()
