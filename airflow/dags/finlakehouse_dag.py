from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion.fmp_ingestion import ingest_fmp_data


def integration_not_configured(integration):
    raise NotImplementedError(
        f"The {integration} integration has not been configured yet."
    )


with DAG(
    dag_id="finlakehouse_daily_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["finance", "lakehouse"],
) as dag:
    ingest_api = PythonOperator(
        task_id="ingest_api",
        python_callable=ingest_fmp_data,
    )
    glue_transform = PythonOperator(
        task_id="glue_transform",
        python_callable=integration_not_configured,
        op_kwargs={"integration": "AWS Glue transformation"},
    )
    load_snowflake = PythonOperator(
        task_id="load_snowflake",
        python_callable=integration_not_configured,
        op_kwargs={"integration": "Snowflake loading"},
    )
    dbt_run = PythonOperator(
        task_id="dbt_run",
        python_callable=integration_not_configured,
        op_kwargs={"integration": "dbt execution"},
    )
    data_quality = PythonOperator(
        task_id="data_quality",
        python_callable=integration_not_configured,
        op_kwargs={"integration": "pipeline data quality"},
    )

    ingest_api >> glue_transform >> load_snowflake >> dbt_run >> data_quality
