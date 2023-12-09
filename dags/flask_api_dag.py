from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.http_hook import HttpHook
from airflow.models import Variable
from airflow.utils.dates import days_ago
import json

def call_flask_api(**kwargs):
    # Retrieve Flask API connection details
    flask_api_conn_id = kwargs.get('flask_api_conn_id', 'flask_api_conn')
    http_hook = HttpHook(http_conn_id=flask_api_conn_id)

    # Retrieve Flask API endpoint from Airflow Variable
    flask_api_endpoint_key = 'http://127.0.0.1:5000/api/data'
    flask_api_endpoint = Variable.get(flask_api_endpoint_key, default_var=None)

    if not flask_api_endpoint:
        raise ValueError(f"Airflow Variable '{flask_api_endpoint_key}' not set.")

    api_endpoint = http_hook.get_connection(flask_api_conn_id).host + flask_api_endpoint

    try:
        response = http_hook.run(api_endpoint, method='GET', headers={}, extra_options=None)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Assuming the API returns JSON data

            # Process the data as needed
            process_data(data)

        else:
            print("Error:", response.status_code, response.text)

    except Exception as e:
        print("Error:", str(e))

def process_data(data):
    # Example: Extract relevant information from the API response
    value = data.get('value')
    timestamp = data.get('timestamp')

    # Perform further processing, logging, or storage of the extracted information
    print("Processed data - Value:", value, "Timestamp:", timestamp)

dag = DAG(
    'flask_api_example',
    schedule_interval='@daily',  # Set your desired schedule interval
    start_date=days_ago(1),
)

flask_api_task = PythonOperator(
    task_id='call_flask_api_task',
    python_callable=call_flask_api,
    provide_context=True,  # Pass the task context to the Python function
    op_args=[],
    op_kwargs={'flask_api_conn_id': 'flask_api_conn'},
    dag=dag,
)

# Add your other tasks here...

flask_api_task  # Set the dependencies appropriately for your other tasks
