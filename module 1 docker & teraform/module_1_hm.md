# Docker and Database Queries: Q&A

## Question 1: Understanding Docker First Run


**Command:**
```bash
docker run -it python:3.12.8 /bin/bash
pip --version
```


**Answer:**
```bash
pip 24.3.1
```

---

## Question 2: Understanding Docker Networking and Docker-Compose

**Answer:**
```yaml
hostname: db
port: 5433
```

---

## Question 3: Trip Segmentation Count

**Query:**
```sql
SELECT
	COUNT(CASE WHEN trip_distance <= 1.0 THEN 1 END) AS below_1,
	COUNT(CASE WHEN trip_distance > 1.0 AND trip_distance <= 3.0 THEN 1 END) AS bet_1_and_3,
	COUNT(CASE WHEN trip_distance > 3.0 AND trip_distance <= 7.0 THEN 1 END) AS bet_3_and_7, 
	COUNT(CASE WHEN trip_distance > 7.0 AND trip_distance <= 10.0 THEN 1 END) AS bet_7_and_10,
	COUNT(CASE WHEN trip_distance > 10.0 THEN 1 END) AS above_10
FROM 
	green_taxi_data
WHERE 
    DATE(lpep_pickup_datetime) >= '2019-10-01' AND
    DATE(lpep_pickup_datetime) < '2019-11-01' AND
    DATE(lpep_dropoff_datetime) >= '2019-10-01' AND
    DATE(lpep_dropoff_datetime) < '2019-11-01';
```

**Answer:**
```plaintext
104,802; 198,924; 109,603; 27,678; 35,189
```

---

## Question 4: Longest Trip for Each Day

**Query:**
```sql
SELECT 
	lpep_pickup_datetime 
FROM
	green_taxi_data
WHERE
	trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_data);
```

**Answer:**
```plaintext
2019-10-31 23:23:41
```

---

## Question 5: Three Biggest Pickup Zones

**Query:**
```sql
SELECT 
	z."Zone", SUM(g."total_amount") AS c
FROM 
	green_taxi_data g
	INNER JOIN taxi_zone_lookup z ON g."PULocationID" = z."LocationID"
	INNER JOIN taxi_zone_lookup x ON g."DOLocationID" = x."LocationID"
WHERE
	g.lpep_pickup_datetime > '2019-10-18'
GROUP BY
	z."Zone"
HAVING
	SUM(g.total_amount) > 13000
ORDER BY 
	c DESC
LIMIT 3;
```

**Answer:**
```plaintext
Top 3 Pickup Zones:
1. [Zone 1]
2. [Zone 2]
3. [Zone 3]
```

---

## Question 6: Largest Tip

**Query:**
```sql
SELECT MAX(g."tip_amount") AS tip, dz."Zone"
FROM green_taxi_data g 
INNER JOIN taxi_zone_lookup pz ON g."PULocationID" = pz."LocationID"
INNER JOIN taxi_zone_lookup dz ON g."DOLocationID" = dz."LocationID"
WHERE
	pz."Zone" = 'East Harlem North'
	AND EXTRACT(YEAR FROM LPEP_PICKUP_DATETIME::DATE) = 2019
	AND EXTRACT(MONTH FROM LPEP_PICKUP_DATETIME::DATE) = 10
GROUP BY
	dz."Zone"
ORDER BY
	tip DESC
LIMIT 1;
```

**Answer:**
```plaintext
87.3 JFK Airport
```

---

## Question 7: Terraform Workflow

**Workflow Steps:**
1. Download provider plugins and set up the backend:
   ```bash
   terraform init
   ```
2. Generate proposed changes and auto-execute the plan:
   ```bash
   terraform apply -auto-approve
   ```
3. Remove all resources managed by Terraform:
   ```bash
   terraform destroy

**Answer:**
```plaintext
terraform init, terraform apply -auto-approve, terraform destroy
```

   
