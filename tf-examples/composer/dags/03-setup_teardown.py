"""Example DAG demonstrating the usage of setup and teardown tasks."""
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

with DAG(
    dag_id="03-setup_teardown",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    BashOperator.as_setup(task_id="root_setup", bash_command="echo 'Hello from root_setup'")
    normal = BashOperator(task_id="normal", bash_command="echo 'I am just a normal task'")
    BashOperator.as_teardown(task_id="root_teardown", bash_command="echo 'Goodbye from root_teardown'")

    with TaskGroup("section_1") as section_1:
        BashOperator.as_setup(task_id="taskgroup_setup", bash_command="echo 'Hello from taskgroup_setup'")
        BashOperator(task_id="normal", bash_command="echo 'I am just a normal task'")
        BashOperator.as_setup(
            task_id="taskgroup_teardown", bash_command="echo 'Hello from taskgroup_teardown'"
        )

    normal >> section_1