import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


def main():
    args = getResolvedOptions(
        sys.argv,
        ["JOB_NAME", "BRONZE_PATH", "SILVER_PATH"],
    )
    spark_context = SparkContext.getOrCreate()
    glue_context = GlueContext(spark_context)
    spark = glue_context.spark_session
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    silver_data = spark.read.parquet(args["BRONZE_PATH"])
    required_keys = [
        column
        for column in ("ticker", "trade_date")
        if column in silver_data.columns
    ]
    if required_keys:
        silver_data = silver_data.na.drop(subset=required_keys)
        silver_data = silver_data.dropDuplicates(required_keys)

    for source_column, target_column in (
        ("open", "open_price"),
        ("close", "close_price"),
    ):
        if source_column in silver_data.columns:
            silver_data = silver_data.withColumnRenamed(
                source_column,
                target_column,
            )

    silver_data.write.mode("errorifexists").parquet(args["SILVER_PATH"])

    job.commit()


if __name__ == "__main__":
    main()
