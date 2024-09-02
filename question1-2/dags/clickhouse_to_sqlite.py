import pandas as pd
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
    def data_from_clickhouse():
        # connect to clickhouse and fetch data
        client = clickhouse_connect.get_client(
            host= os.getenv('host'), 
            user=os.getenv('user'), 
            password=os.getenv('password'), 
            port=int(os.getenv('port')),
            secure=True)
        
        with open(DATA_PATH.joinpath('question1.sql'), 'r') as sql_file:
            query = sql_file.read()
        data = client.query(query)
        list_of_rows = data.result_rows
        list_of_columns = data.column_names

        data_df = pd.DataFrame(list_of_rows, columns=list_of_columns)
        return data_df
    
    @task
    def load_to_sqlite(data):
        # connect to sqlite db
        sqlite_hook = SqliteHook(sqlite_conn_id='sqlite_conn')
        conn = sqlite_hook.get_conn()
        cursor = conn.cursor()
        
        try:
            # create table
            columns = data.columns
            column_defs = ', '.join([f"{col} TEXT" for col in columns])
            create_table_query = f"CREATE TABLE IF NOT EXISTS trip_data ({column_defs});"
            cursor.execute(create_table_query)

            # insert data
            placeholders = ', '.join(['?'] * len(columns))
            insert_query = f"INSERT INTO trip_data ({', '.join(columns)}) VALUES ({placeholders});"
            cursor.executemany(insert_query, data.values.tolist())
            conn.commit()
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    extract_data = data_from_clickhouse()
    load_to_sqlite(extract_data)

clickhouse_to_sqlite()