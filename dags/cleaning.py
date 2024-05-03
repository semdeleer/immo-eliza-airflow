from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime
from random import randint
from immoweb.pipeline.clean import clean_data
from immoweb.model.trainb import make_model

def _cleaning_data():
    clean_data()

def _make_models():
    make_model()


with DAG("clean_model_dag", start_date=datetime(2024,4,25), schedule_interval="@daily", catchup=False) as dag:
    clean_data_task = PythonOperator(
        task_id='cleaning_data',
        python_callable=_cleaning_data,  # Pass the callable function
        dag=dag
    )

    model_making_task = PythonOperator(
        task_id='making_model',
        python_callable=_make_models,  # Pass the callable function
        dag=dag
    )

    clean_data_task >> model_making_task 
