#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd
from sqlalchemy import create_engine
import os
import wget

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_csv('output.csv')

    df.head(0).to_sql(name=table_name,con=engine,if_exists='replace')


    df_iter = pd.read_csv('output.csv' , iterator=True , chunksize=100000)



    while True:
        df= next(df_iter)
        df.to_sql(name=table_name,con=engine,if_exists='append')
        print('successful iteration')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ingest csv data to postgres')

    parser.add_argument('--user', help='user name of postgres')
    parser.add_argument('--password', help='passowrd of postgres')
    parser.add_argument('--host', help='host of postgres')
    parser.add_argument('--port', help='port of postgres')
    parser.add_argument('--db', help='database name of postgres')
    parser.add_argument('--table_name', help='name of the table we will write to')
    parser.add_argument('--url', help='url of csv file')
    args = parser.parse_args()
    
    main(args)
