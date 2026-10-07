import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


def main():
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "RAW_PATH", "BRONZE_PATH"])
    spark_context = SparkContext.getOrCreate()
    glue_context = GlueContext(spark_context)
    spark = glue_context.spark_session
    job = Job(glue_context)
    job.init(args["JOB_NAME"], args)

    raw_data = (
        spark.read
        .option("multiLine", "true")
        .json(args["RAW_PATH"])
    )
    raw_data.write.mode("errorifexists").parquet(args["BRONZE_PATH"])

    job.commit()


if __name__ == "__main__":
    main()
