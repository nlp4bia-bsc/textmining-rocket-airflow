import airflow
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.text_processing.basic_processing import (
    copy_files,
    force_unix_newlines,
    process_file,
)

dag = DAG(
    dag_id="file_process_dag",
    start_date=datetime.datetime(2024, 5, 10),
    schedule_interval=None,
)

# Step 1: Copy files to destination folder
copy_files_step = PythonOperator(
    task_id = "copy_files_step",
    python_callable=copy_files,
    op_kwargs={
        "source_dir": "/opt/airflow/storage/init",
        "dest_dir": "/opt/airflow/storage/dest"
    },
    dag=dag
)

# Step 2: Force unix newlines
force_unix_newlines_step = PythonOperator(
    task_id='force_unix_newlines_step',
    python_callable=force_unix_newlines,
    op_kwargs={
        "output_dir": "/opt/airflow/storage/dest"
    },
    dag=dag
)

copy_files_step >> force_unix_newlines_step