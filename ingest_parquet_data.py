#!/usr/bin/env python
# coding: utf-8
import argparse
import pandas as pd
from sqlalchemy import create_engine
import os
#import wget


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    parquet_name = 'output.parquet'

    os.system(f"wget {url} -O {parquet_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_parquet('output.parquet')

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(0).to_sql(name=table_name,con=engine,if_exists='replace')

    df.to_sql(name=table_name,con=engine,if_exists='append')
    
    print('successful iteration')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ingest parquet data to postgres')

    parser.add_argument('--user', help='user name of postgres')
    parser.add_argument('--password', help='passowrd of postgres')
    parser.add_argument('--host', help='host of postgres')
    parser.add_argument('--port', help='port of postgres')
    parser.add_argument('--db', help='database name of postgres')
    parser.add_argument('--table_name', help='name of the table we will write to')
    parser.add_argument('--url', help='url of parquet file')
    args = parser.parse_args()
    
    main(args)
