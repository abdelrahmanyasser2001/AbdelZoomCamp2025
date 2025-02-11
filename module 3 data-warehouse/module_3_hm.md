# Module 3 Homework

### Question 1: Count of records for the 2024 Yellow Taxi Data
- 65,623  
- 840,402   
- 20,332,093 ✅ 
- 85,431,289 

### Question 2: Estimated amount of data
- 18.82 MB for the External Table and 47.60 MB for the Materialized Table  
- 0 MB for the External Table and 155.12 MB for the Materialized Table ✅  
- 2.14 GB for the External Table and 0MB for the Materialized Table  
- 0 MB for the External Table and 0MB for the Materialized Table  

### Question 3: Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed. ✅ 
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.  
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.  
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed.  

### Question 4: How many records have a fare_amount of 0?
- 128,210  
- 546,578  
- 20,188,016  
- 8,333 ✅ 

### Question 5: The best strategy to make an optimized table in BigQuery
- Partition by tpep_dropoff_datetime and Cluster on VendorID ✅   
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID  
- Cluster on tpep_dropoff_datetime Partition by VendorID  
- Partition by tpep_dropoff_datetime and Partition by VendorID

### Question 6: Estimated processed bytes
- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table  
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table ✅  
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table  
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

### Question 7: Where is the data for external tables stored?
- Big Query  
- Container Registry  
- GCP Bucket ✅  
- Big Table

### Question 8: Always clustering
- True
- False ✅ 
