# airflow_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys

# Add the directory containing your fine-tuning script to the Python path
sys.path.append("C:\Users\bhatt\Desktop\Project\ats_scripts\speechbrain\fine_tuning_script.py")

# Import the fine-tuning script
from fine_tuning_script import fine_tune_tacotron2

# Define default_args for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'speech_fine_tuning',
    default_args=default_args,
    description='Fine-tuning Tacotron2 with SpeechBrain',
    schedule_interval=timedelta(days=1),  # Set the desired schedule interval
)

# Define a Python operator for fine-tuning task
fine_tuning_operator = PythonOperator(
    task_id='fine_tuning_task',
    python_callable=fine_tune_tacotron2,
    op_args=[tacotron2, audio_data, labels, 5],  # Pass necessary arguments to the fine-tuning function
    dag=dag,
)

# Set the task dependencies
fine_tuning_operator
