import duckdb
import os

# Get credentials from your AWS CLI
access_key = os.popen('aws configure get aws_access_key_id').read().strip()
secret_key = os.popen('aws configure get aws_secret_access_key').read().strip()

# Initialize DuckDB
con = duckdb.connect('nyc_taxi.db')

# Install and load the httpfs extension to talk to S3
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Configure S3 access
con.execute(f"SET s3_access_key_id='{access_key}';")
con.execute(f"SET s3_secret_access_key='{secret_key}';")
con.execute("SET s3_region='us-east-1';")

print("--- Creating Analytics Tables ---")

# This one command reads ALL parquet files from S3 and creates a local table
con.execute("""
    CREATE OR REPLACE TABLE trips_raw AS 
    SELECT * FROM read_parquet('s3://nyctaxi-raw-zone-sugali/yellow_taxi/2023/*.parquet');
""")

# Perform the transformation (Calculated trip duration and cleaning)
con.execute("""
    CREATE OR REPLACE TABLE trips_cleaned AS
    SELECT 
        VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        PULocationID,
        DOLocationID,
        fare_amount,
        -- Calculate duration in minutes
        date_diff('minute', tpep_pickup_datetime, tpep_dropoff_datetime) as trip_duration_minutes
    FROM trips_raw
    WHERE passenger_count > 0 AND trip_distance > 0;
""")

print("--- Sample Analytics ---")
# Let's run a quick query to test
result = con.execute("""
    SELECT 
        PULocationID, 
        avg(trip_duration_minutes) as avg_duration 
    FROM trips_cleaned 
    GROUP BY 1 
    ORDER BY 2 DESC 
    LIMIT 5
""").df()

print(result)
print("\nWarehouse ready! File saved as 'nyc_taxi.db'")