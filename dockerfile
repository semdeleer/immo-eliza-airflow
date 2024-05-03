FROM apache/airflow:2.9.0
ADD requirements.txt .
RUN pip install -r requirements.txt
