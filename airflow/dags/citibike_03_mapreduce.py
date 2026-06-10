from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from citibike_airflow_lib import MAPREDUCE_JOBS, run_mapreduce_job, write_mapreduce_report


@dag(
    dag_id="citibike_03_mapreduce",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["citibike", "pipeline", "03_mapreduce"],
)
def citibike_03_mapreduce():
    previous = None
    job_tasks = []

    for job_id, input_path, _table in MAPREDUCE_JOBS:
        @task(task_id=f"run_{job_id}")
        def run_one_mapreduce_job(job_name=job_id, hdfs_input=input_path):
            return run_mapreduce_job(job_name, hdfs_input)

        current = run_one_mapreduce_job()
        job_tasks.append(current)
        if previous is not None:
            previous >> current
        previous = current

    @task
    def summarize(results):
        return write_mapreduce_report(results)

    trigger_next = TriggerDagRunOperator(
        task_id="trigger_citibike_04_export_reports",
        trigger_dag_id="citibike_04_export_reports",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    summarize(job_tasks) >> trigger_next


citibike_03_mapreduce()
