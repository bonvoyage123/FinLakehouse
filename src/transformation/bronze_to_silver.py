from pathlib import Path

from pyspark.sql import SparkSession


def build_spark_session(app_name="FinLakehouse"):
    return SparkSession.builder.appName(app_name).master("local[*]").getOrCreate()


def read_bronze_parquet(spark, bronze_path):
    return spark.read.parquet(str(bronze_path))


def clean_stock_prices(df):
    df = df.na.drop(subset=["ticker", "trade_date"])
    df = df.withColumnRenamed("open", "open_price")
    df = df.withColumnRenamed("close", "close_price")
    return df
