# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, unix_timestamp, round
# import os

# def patch_native_io():
#     """ This function bypasses the Windows NativeIO error in Spark """
#     try:
#         import sys
#         from pyspark import SparkContext
        
#         # This reaches into the Java Virtual Machine to trick the NativeIO class
#         sc = SparkContext.getOrCreate()
#         java_import(sc._gateway.jvm, "org.apache.hadoop.io.nativeio.NativeIO")
#         # We tell the JVM that the 'access' check should always return True
#     except:
#         pass

# # Initialize Spark Session
# spark = SparkSession.builder \
#     .appName("NYCTaxiProcessing") \
#     .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
#     .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
#     .config("spark.hadoop.fs.s3a.access.key", os.popen('aws configure get aws_access_key_id').read().strip()) \
#     .config("spark.hadoop.fs.s3a.secret.key", os.popen('aws configure get aws_secret_access_key').read().strip()) \
#     .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
#     .getOrCreate()

# # --- ACTUAL PROCESSING LOGIC ---
# raw_path = "s3a://nyctaxi-raw-zone-sugali/yellow_taxi/2023/*.parquet"
# staging_path = "s3a://nyctaxi-staging-zone-sugali/yellow_taxi/processed_data/"

# print("--- Starting Spark Job ---")
# df = spark.read.parquet(raw_path)

# cleaned_df = df.filter((col("passenger_count") > 0) & (col("trip_distance") > 0)) \
#     .withColumn("trip_duration_minutes", 
#                 round((unix_timestamp("tpep_dropoff_datetime") - 
#                        unix_timestamp("tpep_pickup_datetime")) / 60, 2))

# cleaned_df.write.mode("overwrite").parquet(staging_path)
# print("--- Job Completed Successfully! ---")


from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, round
import os

# Initialize Spark with the NativeIO bypass and credentials
spark = SparkSession.builder \
    .appName("NYCTaxiProcessing") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.io.nativeio.NativeIO.Windows.access0", "true") \
    .config("spark.driver.extraJavaOptions", "-Dhadoop.home.dir=C:/hadoop") \
    .getOrCreate()

# Ensure the JVM itself knows about the bypass
spark._jvm.org.apache.hadoop.io.nativeio.NativeIO.Windows.access0 = True

# Force credentials into the Hadoop configuration
access_key = os.popen('aws configure get aws_access_key_id').read().strip()
secret_key = os.popen('aws configure get aws_secret_access_key').read().strip()

sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.amazonaws.com")

# Paths
raw_path = "s3a://nyctaxi-raw-zone-sugali/yellow_taxi/2023/*.parquet"
staging_path = "s3a://nyctaxi-staging-zone-sugali/yellow_taxi/processed_data/"

print("--- Loading Data ---")
df = spark.read.parquet(raw_path)

print(f"Initial row count: {df.count()}")

# Minimal Transformation (Just to ensure it works)
processed_df = df.withColumn("trip_duration_minutes", 
                round((unix_timestamp("tpep_dropoff_datetime") - 
                       unix_timestamp("tpep_pickup_datetime")) / 60, 2))

print("--- Writing to Staging ---")
# Using coalesce(1) makes it easier to see the output file (it saves as 1 file)
processed_df.coalesce(1).write.mode("overwrite").parquet(staging_path)

print("--- Job Finished! ---")