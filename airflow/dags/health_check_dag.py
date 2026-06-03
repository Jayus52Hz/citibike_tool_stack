from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator


@dag(
    dag_id="tool_stack_health_check",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["bigdata", "test"],
)
def tool_stack_health_check():
    bash_health = BashOperator(
        task_id="bash_health",
        bash_command="echo airflow-ok && hostname",
    )

    @task
    def python_one_row():
        row = {"id": 1, "name": "test", "value": 100}
        print(row)
        return row

    bash_health >> python_one_row()


tool_stack_health_check()
