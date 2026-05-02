from pyspark.sql import SparkSession
import os

spark = SparkSession.builder.appName("Debug").getOrCreate()

# Load just ONE file to see what's inside
path = "s3a://nyctaxi-raw-zone-sugali/yellow_taxi/2023/yellow_tripdata_2023-01.parquet"
df = spark.read.parquet(path)

print("Total rows in Raw:", df.count())
df.printSchema() # This shows us the column names
df.show(5) # This shows us the first 5 rows