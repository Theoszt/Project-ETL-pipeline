from celery import Celery
from kombu import Exchange, Queue
from pre_processing import preprocess_data
from feature_engineering import feature_engineer
import pandas as pd
from io import StringIO
from RDBMS import save_to_postgres
import json
app = Celery(
    'etl_tasks',
    broker='pyamqp://guest:guest@localhost:5672//', 
    backend='rpc://'
)
app.conf.task_queues = (
    Queue(
        name='pre_proses',
        exchange=Exchange('preprocessing', type='direct'),
        routing_key='pre_proses'
    ),
    Queue(
        name='feature_engineering',
        exchange=Exchange('featureengineering', type='direct'),
        routing_key='feature_engineering'
    )
)


app.conf.task_routes = {
    'tasks.preprocess': {'queue': 'pre_proses', 'routing_key': 'pre_proses'},
    'tasks.feature_engineering': {'queue': 'feature_engineering', 'routing_key': 'feature_engineering'},
}

@app.task(name='tasks.preprocess',queue='pre_proses')
def preprocess(data):
    cleaned_data = preprocess_data(data)
    return cleaned_data

@app.task(name='tasks.feature_engineering', queue='feature_engineering')
def feature_engineering(cleaned_data: str):
    df = pd.read_json(StringIO(cleaned_data), orient='split')  
    df_processed = feature_engineer(df)
    save_to_postgres(df_processed)
    df_processed.to_csv('fitur.csv')
    return df_processed.to_json(orient='split')
