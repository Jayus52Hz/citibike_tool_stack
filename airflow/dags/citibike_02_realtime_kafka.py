from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from citibike_airflow_lib import (
    build_realtime_image,
    consume_realtime_messages,
    prepare_realtime_table_and_topic,
    publish_realtime_messages,
    validate_realtime,
)


@dag(
    dag_id="citibike_02_realtime_kafka",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["citibike", "pipeline", "02_realtime"],
)
def citibike_02_realtime_kafka():
    @task
    def build_runtime_image():
        build_realtime_image()

    @task
    def reset_topic_and_table():
        prepare_realtime_table_and_topic()

    @task
    def publish_messages():
        publish_realtime_messages(max_records=200)

    @task
    def consume_messages():
        return consume_realtime_messages(max_records=200)

    @task
    def validate_and_report(group_id):
        return validate_realtime(group_id=group_id)

    trigger_next = TriggerDagRunOperator(
        task_id="trigger_citibike_03_mapreduce",
        trigger_dag_id="citibike_03_mapreduce",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    built = build_runtime_image()
    reset = reset_topic_and_table()
    published = publish_messages()
    group_id = consume_messages()

    built >> reset >> published >> group_id
    validate_and_report(group_id) >> trigger_next


citibike_02_realtime_kafka()
