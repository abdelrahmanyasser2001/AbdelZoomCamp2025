from airflow import DAG
from datetime import datetime , timedelta
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.http.sensors.http import HttpSensor 
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, get_current_context
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator




import os
import tarfile
import pandas as pd
import shutil


_SNOWFLAKE_CONN_ID = "snowflake_conn"
_SNOWFLAKE_TABLE = "SRC_TEMP"
_SNOWFLAKE_STAGING_TABLE = "SRC_STAGING"

OUTPUT_DIR = "/tmp/compressed"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_config_parameters(**kwargs):
  context = get_current_context()
  tmp_year = kwargs["dag_run"].conf.get('year')
  print(tmp_year)
  kwargs['ti'].xcom_push(key='year', value=tmp_year)


def uncompress_response(response):
  compressed_file_path = os.path.join(OUTPUT_DIR, "data.tar.gz")
  with open(compressed_file_path, "wb") as f:
    f.write(response.content)
  with tarfile.open(compressed_file_path, "r:gz") as tar:
    tar.extractall(path=OUTPUT_DIR)
    os.remove(compressed_file_path)
  return OUTPUT_DIR



def insert_into_snowflake(filepath, snowflake_conn_id=_SNOWFLAKE_CONN_ID):
    hook = SnowflakeHook(snowflake_conn_id=_SNOWFLAKE_CONN_ID)
    engine = hook.get_sqlalchemy_engine()

    for filename in os.listdir(filepath):
        file_path = os.path.join(filepath, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            print(f"Processing file: {file_path}")
            
            df = pd.read_csv(file_path)

            unwanted_columns = {'unique_row_id', 'filename'}
            df = df[[col for col in df.columns if col not in unwanted_columns]]

            df.columns = [col.lower() for col in df.columns]
            df.to_sql(_SNOWFLAKE_STAGING_TABLE, engine, if_exists='append', index=False)
            print(f"Inserted {len(df)} rows from {filename} into {_SNOWFLAKE_STAGING_TABLE}.")

    shutil.rmtree('/tmp/compressed')



CREATE_STAGING_TABLE_SQL_STRING= (
    f'''CREATE TABLE IF NOT EXISTS {_SNOWFLAKE_STAGING_TABLE} (
          unique_row_id        TEXT,
          STATION              BIGINT,
          DATE                 TIMESTAMP,
          SOURCE               BIGINT,
          LATITUDE             DOUBLE PRECISION,
          LONGITUDE            DOUBLE PRECISION,
          ELEVATION            DOUBLE PRECISION,
          NAME                 TEXT,
          REPORT_TYPE          TEXT,
          CALL_SIGN            BIGINT,
          QUALITY_CONTROL      TEXT,
          WND                  TEXT,
          CIG                  TEXT,
          VIS                  TEXT,
          TMP                  TEXT,
          DEW                  TEXT,
          SLP                  TEXT,
          GF1                  TEXT,
          MW1                  TEXT,
          EQD                  TEXT);'''

)

CREATE_TABLE_SQL_STRING= (
    f'''CREATE TABLE IF NOT EXISTS {_SNOWFLAKE_TABLE} (
          unique_row_id        TEXT,
          STATION              BIGINT,
          DATE                 TIMESTAMP,
          SOURCE               BIGINT,
          LATITUDE             DOUBLE PRECISION,
          LONGITUDE            DOUBLE PRECISION,
          ELEVATION            DOUBLE PRECISION,
          NAME                 TEXT,
          REPORT_TYPE          TEXT,
          CALL_SIGN            BIGINT,
          QUALITY_CONTROL      TEXT,
          WND                  TEXT,
          CIG                  TEXT,
          VIS                  TEXT,
          TMP                  TEXT,
          DEW                  TEXT,
          SLP                  TEXT,
          GF1                  TEXT,
          MW1                  TEXT,
          EQD                  TEXT);'''

)

TRUNCATE_STAGING= (f'TRUNCATE TABLE {_SNOWFLAKE_STAGING_TABLE};')

SET_UNIQUE_ROW_ID= (
    f'''UPDATE {_SNOWFLAKE_STAGING_TABLE}
        SET unique_row_id = MD5_HEX(
            COALESCE(STATION, '') || 
            COALESCE(TO_VARCHAR(DATE), '') || 
            COALESCE(TO_VARCHAR(LATITUDE), '') || 
            COALESCE(TO_VARCHAR(LONGITUDE), '') || 
            COALESCE(REPORT_TYPE, '') || 
            COALESCE(SOURCE, '')
        )
        WHERE unique_row_id IS NULL;
    '''
    )

MOVE_TO_MAIN_TABLE= (
    f'''
    INSERT INTO {_SNOWFLAKE_TABLE} (
        unique_row_id, 
        STATION, 
        DATE, 
        SOURCE, 
        LATITUDE, 
        LONGITUDE, 
        ELEVATION, 
        NAME, 
        REPORT_TYPE, 
        CALL_SIGN, 
        QUALITY_CONTROL, 
        WND, 
        CIG, 
        VIS, 
        TMP, 
        DEW, 
        SLP, 
        GF1, 
        MW1, 
        EQD
    )
    SELECT 
        s.unique_row_id, 
        s.STATION, 
        s.DATE, 
        s.SOURCE, 
        s.LATITUDE, 
        s.LONGITUDE, 
        s.ELEVATION, 
        s.NAME, 
        s.REPORT_TYPE, 
        s.CALL_SIGN, 
        s.QUALITY_CONTROL, 
        s.WND, 
        s.CIG, 
        s.VIS, 
        s.TMP, 
        s.DEW, 
        s.SLP, 
        s.GF1, 
        s.MW1, 
        s.EQD
    FROM {_SNOWFLAKE_STAGING_TABLE} s
    LEFT JOIN {_SNOWFLAKE_TABLE} m
    ON s.unique_row_id = m.unique_row_id
    WHERE m.unique_row_id IS NULL;
    '''
    )



with DAG('snowflake_dag',
        start_date=datetime(2025, 1, 23),
        default_args={"snowflake_conn_id": _SNOWFLAKE_CONN_ID},
        schedule_interval='@daily',
        catchup=False,
        tags=['nada'],
        ) as dag:

  config_parameters = PythonOperator( task_id = "DAG_CONFIG_PARAMS", python_callable = get_config_parameters) 

  create_staging_table = SnowflakeOperator(task_id="create_src_stage", sql=CREATE_STAGING_TABLE_SQL_STRING)
  
  create_temp_table = SnowflakeOperator(task_id="create_src_temp", sql=CREATE_TABLE_SQL_STRING)
  
  truncate_staging_table = SnowflakeOperator(task_id="truncate_staging_table", sql=TRUNCATE_STAGING)

  
  is_link_avalible = HttpSensor(
        task_id='is_link_avalible',
        http_conn_id='http_ncei',
        endpoint='/data/global-hourly/archive/csv/{{ task_instance.xcom_pull(task_ids="DAG_CONFIG_PARAMS", key="year") }}.tar.gz',
  )

  extract_data = SimpleHttpOperator(
        task_id='extract_data',
        http_conn_id='http_ncei',
        endpoint='data/global-hourly/archive/csv/{{ task_instance.xcom_pull(task_ids="DAG_CONFIG_PARAMS", key="year") }}.tar.gz',
        method='GET',
        response_filter=uncompress_response,
  )


  verify_output = BashOperator(
        task_id='verify_output',
        bash_command=f'ls -l {OUTPUT_DIR}' 
  )

  
  load_data = PythonOperator(
      task_id='load_data',
      python_callable=insert_into_snowflake,
      op_kwargs={'filepath': OUTPUT_DIR, 'conn_id': 'postgres'},
      
  )

  update_unique_row_id = SnowflakeOperator(task_id="update_unique_row_id", sql=SET_UNIQUE_ROW_ID)


  move_data_to_main = SnowflakeOperator(task_id='move_data_to_main', sql=MOVE_TO_MAIN_TABLE)
    



config_parameters >> create_staging_table >> create_temp_table >> truncate_staging_table >> is_link_avalible >> extract_data >> verify_output  >> load_data >> update_unique_row_id >> move_data_to_main
