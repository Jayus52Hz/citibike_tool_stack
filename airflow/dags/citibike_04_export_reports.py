from datetime import datetime

from airflow.decorators import dag, task

from citibike_airflow_lib import (
    MAPREDUCE_JOBS,
    export_mapreduce_job,
    prepare_report_tables,
    write_export_report,
)


@dag(
    dag_id="citibike_04_export_reports",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["citibike", "pipeline", "04_export_reports"],
)
def citibike_04_export_reports():
    @task
    def create_report_tables():
        prepare_report_tables()

    previous = create_report_tables()
    export_tasks = []

    for job_id, _input_path, table in MAPREDUCE_JOBS:
        @task(task_id=f"export_{job_id}")
        def export_one(job_name=job_id, report_table=table):
            return export_mapreduce_job(job_name, report_table)

        current = export_one()
        export_tasks.append(current)
        previous >> current
        previous = current

    @task
    def summarize(results):
        return write_export_report(results)

    summarize(export_tasks)


citibike_04_export_reports()
