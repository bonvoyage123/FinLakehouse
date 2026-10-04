from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def extract_market_data():
    """Placeholder task for API extraction logic."""
    print("Extracting market data from the upstream financial API...")


def transform_bronze_to_silver():
    """Placeholder task for bronze/silver processing."""
    print("Transforming raw data into the silver layer...")


def load_gold_models():
    """Placeholder task for dbt or warehouse loading."""
    print("Loading analytical gold models...")


with DAG(
    dag_id="finlakehouse_daily_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["finance", "lakehouse"],
) as dag:
    start = EmptyOperator(task_id="start")
    extract = PythonOperator(task_id="extract_data", python_callable=extract_market_data)
    bronze = PythonOperator(task_id="bronze_layer", python_callable=transform_bronze_to_silver)
    gold = PythonOperator(task_id="gold_layer", python_callable=load_gold_models)
    end = EmptyOperator(task_id="end")

    start >> extract >> bronze >> gold >> end
