from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator
from airflow.utils import trigger_rule
import os

DEFAULT_CLUSTER_NAME = 'etl-default-cluster'
DEFAULT_ENV = os.getenv('COMPOSER_ENVIRONMENT').split('-')[-1]
DEFAULT_CLUSTER_PROJECT = os.getenv('GCP_PROJECT', 'staging')
DEFAULT_CLUSTER_REGION = os.getenv('COMPOSER_LOCATION', 'us-west1')
DEFAULT_METASTORE = f'metastore-{DEFAULT_ENV}-usw1'
DEFAULT_CLUSTER_WORKERS = 2
DEFAULT_CLUSTER_ZONE = 'us-west1-a'
DEFAULT_SSH_KEY_DURATION = '30s'
DEFAULT_SUBNET = Variable.get('subnet', f'shared_vpc_subnet')
DEFAULT_VERSION = Variable.get('etl_util')
DEFAULT_MACHINE_TYPE = 'n2d-highmem-16'
LOCAL_VERSION = __file__.split('/')[-2]
INITIALIZATION_SCRIPT = "gs://{GCP_BUCKET}/etl_util/init_env.sh"

def is_active_version():
    return LOCAL_VERSION == DEFAULT_VERSION

def create_cluster(dag, name=DEFAULT_CLUSTER_NAME, workers=DEFAULT_CLUSTER_WORKERS, zone=DEFAULT_CLUSTER_ZONE,
                    region=DEFAULT_CLUSTER_REGION, project=DEFAULT_CLUSTER_PROJECT, subnet=DEFAULT_SUBNET,
                    metastore=DEFAULT_METASTORE, version=DEFAULT_VERSION, env=DEFAULT_ENV, 
                    machine_type=DEFAULT_MACHINE_TYPE):
    command = f"""
    gcloud beta dataproc clusters create {name} \
        --enable-component-gateway \
        --region {region} \
        --subnet {subnet} \
        --zone {zone} \
        --master-machine-type {machine_type} \
        --master-boot-disk-size 500 \
        --num-workers {workers} \
        --worker-machine-type {machine_type} \
        --worker-boot-disk-size 500 \
        --image-version 2.0-ubuntu18 \
        --max-idle 15m \
        --initialization-actions {INITIALIZATION_SCRIPT} \
        --properties ^#^hive:hive.execution.engine=mr#hive:hive.metastore.warehouse.dir=gs://{metastore}/hive/warehouse#hive:hive.aux.jars.path=file:///usr/lib/hive/jars/somejar.jar,gs://{GCP_BUCKET}/dependencies/custom-udfs.jar#hive:hive.metastore.uri=thrift://{THRIFT_IP_ADDRESS}:9083#presto:query.max-memory-per-node=72000MB#presto:query.max-total-memory-per-node=72000MB# \
        --dataproc-metastore projects/{project}/locations/{region}/services/{metastore} \
        --scopes 'https://www.googleapis.com/auth/cloud-platform' \
        --project {project} \
        --scopes cloud-platform \
        --metadata version={version},env={env} \
        --optional-components=PRESTO
    """
    return BashOperator(task_id='create_cluster', bash_command=command, dag=dag)

def remote_ssh_command(command, cluster=DEFAULT_CLUSTER_NAME, zone=DEFAULT_CLUSTER_ZONE, key_duration=DEFAULT_SSH_KEY_DURATION):
    return f'gcloud beta compute ssh {cluster}-m --zone {zone} --tunnel-through-iap --ssh-key-expiry-after {key_duration} --command "{command}"'

def remote_ssh_task(dag, task_id, command, cluster=DEFAULT_CLUSTER_NAME, zone=DEFAULT_CLUSTER_ZONE, key_duration=DEFAULT_SSH_KEY_DURATION):
    return BashOperator(task_id=task_id, bash_command=remote_ssh_command(command, cluster, zone, key_duration), dag=dag)

def remote_pig_sh_script(sciprt, args, cluster=DEFAULT_CLUSTER_NAME, region=DEFAULT_CLUSTER_REGION):
    pig_command = f"sh chmod 750 {script}; sh {script} {' '.join(args)}"
    return f"gcloud dataproc jobs submit pig --cluster {cluster} --region {region} -e '{pig_command}'"

def remote_pig_sh_task(dag, task_id, script, args, cluster=DEFAULT_CLUSTER_NAME, regions=DEFAULT_CLUSTER_REGION):
    return BashOperator(task_id=task_id, bash_command=remote_pig_sh_script(script, args, cluster, region), dag=dag)

def cluster_cleanup(dag, cluster=DEFAULT_CLUSTER_NAME, dependencies=[], region=DEFAULT_CLUSTER_REGION, project=DEFAULT_CLUSTER_PROJECT):
    delete_task = DataprocDeleteClusterOperator(
        task_id='delete_cluster',
        cluster_name=cluster,
        region=region,
        project_id=project,
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE,
        dag=dag
    )
    catch_task = DummyOperator(task_id='catch_failure', dag=dag, trigger_rule=trigger_rule.TriggerRule.NONE_FAILED)
    for upstream in dependencies:
        delete_task.set_upstream(upstream)
        catch_task.set_upstream(upstream)
    return delete_task, catch_task