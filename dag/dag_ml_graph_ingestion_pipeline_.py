
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 5, 9),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='ml_graph_ingestion_pipeline_', default_args=default_args,
    schedule_interval='0 8 * * 5', )

sendNotification = DummyOperator(
    task_id='send_notification',
    default_args=default_args,
    dag=dag,
)

#SparkSubmitOperator(
ingesting_row_data_HIVE = DummyOperator(
    task_id='ingesting_row_data_HIVE',
    default_args=default_args,
    dag=dag,
)

#SparkSubmitOperator(
ingesting_graph_HBASE = DummyOperator(
    task_id='ingesting_graph_HBASE',
    default_args=default_args,
    dag=dag,
)

def decide_which_path():
    if True:
        return "branch_a"
    else:
        return "branch_b"


branch_checkForChanges = BranchPythonOperator(
    task_id='check_data_availablity',
    python_callable=decide_which_path,
    trigger_rule="all_done",
    dag=dag)

branch_checkForChanges.set_downstream(ingesting_row_data_HIVE)
branch_checkForChanges.set_downstream(sendNotification)
ingesting_row_data_HIVE.set_downstream(ingesting_graph_HBASE)
ingesting_graph_HBASE.set_downstream(sendNotification)

