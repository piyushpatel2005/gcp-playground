import airflow
from builtins import range
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
from datetime import timedelta


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='00-bash_example', default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60))

cmd = 'ls -l'
run_this_last = DummyOperator(task_id='run_this_last', dag=dag)

run_this = BashOperator(
    task_id='run_after_loop', bash_command='echo 1', dag=dag)
run_this.set_downstream(run_this_last)
# run_after_loop >> run_this_last

# Create 3 tasks, down sream is run_this
# runme_1 >> run_after_loop
# runme_2 >> run_after_loop
# rumme_3 >> run_after_loop
for i in range(3):
    i = str(i)
    task = BashOperator(
        task_id='runme_'+i,
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        dag=dag)
    task.set_downstream(run_this)

task = BashOperator(
    task_id='also_run_this',
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag)
task.set_downstream(run_this_last)
# also_run_this >> run_this_last

if __name__ == "__main__":
    dag.cli()