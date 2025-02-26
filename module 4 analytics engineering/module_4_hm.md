# module 4 hm

## Question 1: Model Resolution (1 point)
**Possible Answers:**  
- ❌ `SELECT * FROM dtc_zoomcamp_2025.raw_nyc_tripdata.ext_green_taxi`  
- ❌ `SELECT * FROM dtc_zoomcamp_2025.my_nyc_tripdata.ext_green_taxi`  
- ✅ **`SELECT * FROM myproject.raw_nyc_tripdata.ext_green_taxi`** (Correct)  
- ❌ `SELECT * FROM myproject.my_nyc_tripdata.ext_green_taxi`  
- ❌ `SELECT * FROM dtc_zoomcamp_2025.raw_nyc_tripdata.green_taxi`  

---

## Question 2: Change the Query (1 point)
**Possible Answers:**  
- ❌ `Add ORDER BY pickup_datetime DESC and LIMIT {{ var("days_back", 30) }}`  
- ❌ `Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", 30) }}' DAY`  
- ❌ `Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", "30") }}' DAY`  
- ✅ **`Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY`** (Correct)  
- ❌ `Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", var("days_back", "30")) }}' DAY`  

---

## Question 3: Lineage (1 point)
**Possible Answers:**  
- ❌ `dbt run`  
- ❌ `dbt run --select +models/core/dim_taxi_trips.sql+ --target prod`  
- ❌ `dbt run --select +models/core/fct_taxi_monthly_zone_revenue.sql`  
- ❌ `dbt run --select +models/core/`  
- ✅ **`dbt run --select models/staging/+`** (Correct)  

---

## Question 4: Macros and Jinja (1 point)
✅ **All statements are true except the second one.**  

---

## Question 5: Taxi Quarterly Revenue Growth (1 point)
**Possible Answers:**  
- ❌ `green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q2, worst: 2020/Q1}`  
- ❌ `green: {best: 2020/Q2, worst: 2020/Q1}, yellow: {best: 2020/Q3, worst: 2020/Q4}`  
- ✅ **`green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}`** (Correct)  
- ❌ `green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q1, worst: 2020/Q2}`  
- ❌ `green: {best: 2020/Q1, worst: 2020/Q2}, yellow: {best: 2020/Q3, worst: 2020/Q4}`  

---

## Question 6: P97/P95/P90 Taxi Monthly Fare (1 point)
**Possible Answers:**  
- ❌ `green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}`  
- ✅ **`green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}`** (Correct)  
- ❌ `green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 52.0, p95: 37.0, p90: 25.5}`  
- ❌ `green: {p97: 40.0, p95: 33.0, p90: 24.5}, yellow: {p97: 31.5, p95: 25.5, p90: 19.0}`  
- ❌ `green: {p97: 55.0, p95: 45.0, p90: 26.5}, yellow: {p97: 52.0, p95: 25.5, p90: 19.0}`  

---

## Question 7: Top #Nth Longest P90 Travel Time Location for FHV (2 points)
**Possible Answers:**  
- ✅ **`LaGuardia Airport, Chinatown, Garment District`** (Correct)  
- ❌ `LaGuardia Airport, Park Slope, Clinton East`  
- ❌ `LaGuardia Airport, Saint Albans, Howard Beach`  
- ❌ `LaGuardia Airport, Rosedale, Bath Beach`  
- ❌ `LaGuardia Airport, Yorkville East, Greenpoint`  

---

