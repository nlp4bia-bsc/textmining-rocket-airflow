import airflow
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from text_processing.scripts.basic_processing import (
    copy_files,
    force_unix_newlines,
    remove_html_errors,
    fix_encoding_errors,
)
from text_processing.scripts.quick_prepro import quick_preprosessing
from text_processing.scripts.check_newlines import check_newlines


dag = DAG(
    dag_id="text_processing",
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

# Step 3: Remove common artifacts
fix_encoding_errors_step = PythonOperator(
    task_id='fix_encoding_errors_step',
    python_callable=fix_encoding_errors,
    op_kwargs={
        "output_dir": "/opt/airflow/storage/dest"
    },
    dag=dag
)

# Step 4: Remove common HTML errors
remove_html_errors_step = PythonOperator(
    task_id='remove_html_errors_step',
    python_callable=remove_html_errors,
    op_kwargs={
        "output_dir": "/opt/airflow/storage/dest"
    },
    dag=dag
)

# Step 5: Quick substitution of common errors and Unicode normalization
quick_preprosessing_step = PythonOperator(
    task_id='quick_preprosessing_step',
    python_callable=quick_preprosessing,
    op_kwargs={
        "output_dir": "/opt/airflow/storage/dest"
    },
    dag=dag
)

# Step 6: Check if there are lines starting with lowercase. I need to manually go to those files and correct them if newlines are wrongly added
check_newlines_step = PythonOperator(
    task_id='check_newlines_step',
    python_callable=check_newlines,
    op_kwargs={
        "output_dir": "/opt/airflow/storage/dest"
    },
    dag=dag
)

copy_files_step >> force_unix_newlines_step >> fix_encoding_errors_step >> remove_html_errors_step >> quick_preprosessing_step >> check_newlines_step