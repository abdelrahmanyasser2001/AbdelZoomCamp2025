FROM python:3.9.1

RUN apt-get install wget

RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app

COPY ingest_parquet_data.py ingest_parquet_data.py

ENTRYPOINT [ "python" , "ingest_parquet_data.py" ]
