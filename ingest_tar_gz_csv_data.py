#!/usr/bin/env python
# coding: utf-8

import argparse
import pandas as pd
from sqlalchemy import create_engine
import os
import tarfile
#import wget

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    tar_file_name = 'output.tar.gz'
    extract_dir = 'extracted_csvs'

    os.system(f"wget {url} -O {tar_file_name}")

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    
    with tarfile.open(tar_file_name, "r:gz") as tar:
        tar.extractall(path=extract_dir)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    first_csv_file = None
    for file in os.listdir(extract_dir):
        if file.endswith('.csv'):
            first_csv_file = os.path.join(extract_dir, file)
            break
    
    if first_csv_file is None:
        print("No CSV files found in the extracted archive.")
        return 

    for csv_file in os.listdir(extract_dir):
            if csv_file.endswith('.csv'):
                csv_path = os.path.join(extract_dir, csv_file)
                print(f"Processing file: {csv_file}")
                
                # Read and ingest data in chunks
                df_iter = pd.read_csv(csv_path, iterator=True, chunksize=100000)
                for df_chunk in df_iter:
                    df_chunk.to_sql(name=table_name, con=engine, if_exists='append')
                    print(f"Inserted chunk from '{csv_file}' into table '{table_name}'.")

    print("Data ingestion completed successfully.")


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
