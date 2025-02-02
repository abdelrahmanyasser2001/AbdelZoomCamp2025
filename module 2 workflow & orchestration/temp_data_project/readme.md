# Airflow DAG for NCEI to Snowflake Data Pipeline
This project sets up an Apache Airflow DAG to extract historical temperature data from the National Centers for Environmental Information (NCEI) API and load it into Snowflake for further analysis. The pipeline is enhanced using Astro, a modern data orchestration platform built on top of Airflow, to simplify development, testing, and deployment.
## Overview
This project demonstrates how to:

##### 1. Extract data from the NCEI API.
##### 2. Load the data into Snowflake.
##### 3. Use Astro to streamline the development and deployment of the Airflow DAG.

The pipeline is designed to be configurable, allowing you to specify the year for which data should be processed.







### 1. Snowflake Setup
Execute the following SQL commands in Snowflake to set up roles, warehouses, and schemas:

```sql
USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS TRANS;
GRANT ROLE TRANS TO ROLE ACCOUNTADMIN;
CREATE WAREHOUSE IF NOT EXISTS SNOW_WAREHOUSE;
GRANT OPERATE ON WAREHOUSE SNOW_WAREHOUSE TO ROLE TRANS;
CREATE DATABASE IF NOT EXISTS DATA_ZOOMCAMP;
CREATE SCHEMA IF NOT EXISTS DATA_ZOOMCAMP.RAW;
CREATE SCHEMA IF NOT EXISTS DATA_ZOOMCAMP.DEV;
DROP TABLE IF EXISTS DATA_ZOOMCAMP.RAW.SRC_STAGING;
GRANT ALL ON WAREHOUSE SNOW_WAREHOUSE TO ROLE TRANS;
GRANT ALL ON DATABASE DATA_ZOOMCAMP TO ROLE TRANS;
GRANT ALL ON ALL SCHEMAS IN DATABASE DATA_ZOOMCAMP TO ROLE TRANS;
```

### 2. Configure Airflow
- Add the **HTTP connection** for NCEI in Airflow (`www.ncei.noaa.gov`).
- Add the **Snowflake connection** in Airflow with appropriate credentials.

### 3. Astro Setup
##### 1. Install the Astro CLI:
```bash
apache-airflow-providers-snowflake==5.8.0
```
##### 2. Initialize an Astro project:
```bash
apache-airflow-providers-snowflake==5.8.0
```
##### 3. Add the Snowflake provider to requirements.txt:
```bash
apache-airflow-providers-snowflake==5.8.0
```
##### 4. Start the Astro development environment:
```bash
astro dev start
```

 

##  DAG Configuration
The DAG `snowdag.py` processes data for a configurable year.
Trigger the DAG with a configuration parameter:
```json
{"year":"1901"}
```

## Running the Pipeline
1. Start the Astro development environment:
```bash
astro dev start
```
2. Open the Airflow UI (usually at http://localhost:8080).
3. **Configure the necessary connections:** 

    * **NCEI HTTP Connection:**
        * Conn Id: `ncei_http`
        * Conn Type: `HTTP`
        * Host: `https://www.ncei.noaa.gov`

    * **Snowflake Connection:**
        * Conn Id: `snowflake_conn`
        * Conn Type: `Snowflake`
        * Host: Your Snowflake account URL (e.g., `xy12345.snowflakecomputing.com`).  **Replace with your actual URL.**
        * Schema: `DATA_ZOOMCAMP.RAW`
        * Login: Your Snowflake username. **Replace with your actual username.**
        * Password: Your Snowflake password. **Replace with your actual password.**
        * Extra: `{"role": "TRANS", "warehouse": "SNOW_WAREHOUSE", "database": "DATA_ZOOMCAMP"}`. **Ensure warehouse and database names are correct.**

4. **Trigger the DAG:** Once the connections are configured, trigger the DAG with the desired configuration.




## Notes
* Ensure the Snowflake provider package is installed in Airflow.

* Use Astro's local development environment to simplify testing and debugging.

