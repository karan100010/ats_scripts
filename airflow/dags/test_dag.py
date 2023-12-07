from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'test_DAG_0.1',
    default_args=default_args,
    description='Test DAG for automating the process of language tasks',
    schedule_interval=timedelta(days=1),  # Adjust this as per your requirements
)

check_service_availability = HttpSensor(
    task_id='check_service_availability',
    method='GET',
    http_conn_id='speechbrain_conn_id',  # You need to define a connection in Airflow with your base URL
    endpoint='/api_status',  # Change this endpoint based on your service health check
    response_check=lambda response: response.status_code == 200 and print(response.text),
    poke_interval=60,  # Adjust the interval based on your requirements
    timeout=120,  # Adjust the timeout based on your requirements
    dag=dag,
)

predict_language_task = SimpleHttpOperator(
    task_id='predict_language_task',
    method='POST',
    http_conn_id='speechbrain_conn_id',
    endpoint='/predict_language',
    data='{"filepath": "https://omniglot.com/soundfiles/udhr/udhr_th.mp3"}',
    headers={"Content-Type": "application/json"},
    response_check=lambda response: response.status_code == 200 and print(response.text),
    # response_check=lambda response: response.status_code == 200,
    dag=dag,
)




check_service_availability >> predict_language_task
