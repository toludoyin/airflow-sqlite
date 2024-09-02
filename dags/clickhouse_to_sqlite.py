from airflow.decorators import dag, task
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from pendulum import datetime
import clickhouse_connect
import os
from dotenv import load_dotenv
import pathlib

load_dotenv()
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../data').resolve()

@dag(
   schedule_interval='@once',
    start_date=datetime(2024, 8, 31, tz='UTC'),
    catchup=False,
    tags=['clickhouse-tripdata'],
)

def clickhouse_to_sqlite():
    @task
    def data_from_clickhouse(**kwargs):
        
        client = clickhouse_connect.get_client(
            host= os.getenv('host'), 
            user=os.getenv('user'), 
            password=os.getenv('password'), 
            port=int(os.getenv('port')),
            secure=True)
        
        with open(DATA_PATH.joinpath('Question_1.sql'), 'r') as sql_file:
            query = sql_file.read()

        data = client.query(query).result_rows
        return data

    extract_data = data_from_clickhouse()

clickhouse_to_sqlite()