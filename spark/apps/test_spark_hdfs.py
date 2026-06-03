from pyspark.sql import SparkSession


spark = (
    SparkSession.builder.appName("citibike-tool-stack-hdfs-test")
    .getOrCreate()
)

input_path = "hdfs://namenode:9000/data/test/test.csv"
output_path = "hdfs://namenode:9000/data/test/spark-output"

df = spark.read.option("header", "true").csv(input_path)
df.write.mode("overwrite").option("header", "true").csv(output_path)

print("spark_rows=", df.count())
spark.stop()
