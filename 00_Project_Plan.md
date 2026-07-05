# FinLakehouse: Consolidated Project Plan

## 1. Project Objective

Build a production-style Financial Lakehouse that ingests stock market and company financial data, processes it using a Medallion Architecture, models business-ready datasets, orchestrates the pipeline, and exposes analytics dashboards.

## 2. High-Level Architecture

```mermaid
graph TD
    subgraph "Data Sources"
        A[Financial APIs <br> e.g., Alpha Vantage, Polygon.io]
        B[Public Datasets <br> e.g., SEC EDGAR]
    end

    subgraph "Orchestration (Apache Airflow)"
        direction LR
        O1[Ingestion DAG] --> O2[Processing DAG] --> O3[dbt DAG]
    end

    subgraph "Data Platform (AWS)"
        subgraph "Data Lake (S3)"
            direction LR
            D_Bronze[Bronze Layer <br> Raw Data] --> D_Silver[Silver Layer <br> Cleaned/Partitioned Data] --> D_Gold[Gold Layer <br> Aggregated/Feature Data]
        end

        subgraph "Processing"
            P[Apache Spark (PySpark)]
        end

        subgraph "Data Warehouse"
            DW[Snowflake]
        end
    end

    subgraph "Business Intelligence"
        BI[Analytics Dashboard <br> e.g., Tableau, Power BI]
    end

    %% Defining the flow
    A -- Ingested by --> O1
    B -- Ingested by --> O1

    O1 -- Triggers Python/boto3 script --> D_Bronze

    O2 -- Triggers Spark Job --> P
    P -- Reads from --> D_Bronze
    P -- Cleans & Transforms --> D_Silver
    P -- Aggregates & Models --> D_Gold

    O3 -- Triggers dbt run --> DW
    D_Gold -- Loaded into --> DW

    DW -- Queried by --> BI

    style O1 fill:#e6f3ff,stroke:#333,stroke-width:2px
    style O2 fill:#e6f3ff,stroke:#333,stroke-width:2px
    style O3 fill:#e6f3ff,stroke:#333,stroke-width:2px
```

## 3. Phase-wise Execution Plan

### Phase 1: Foundation and Raw Data Ingestion
*   **Objective:** Establish the project's foundation and build a pipeline to ingest raw data from a source into the Bronze layer of the data lake.
*   **Tech Stack & Roles:**
    *   **Apache Airflow:** Central orchestrator for scheduling and triggering the ingestion pipeline.
    *   **Python (`requests`, `boto3`):** Language for writing the data extraction logic and uploading raw data to S3.
    *   **AWS S3:** Serves as the **Bronze Layer** for storing raw, immutable data.
    *   **Git & GitHub:** For version control.

### Phase 2: Data Cleaning and Processing (Bronze to Silver)
*   **Objective:** Transform the raw data from the Bronze layer into cleaned, structured, and queryable data in the Silver layer.
*   **Tech Stack & Roles:**
    *   **Apache Spark (PySpark):** Core processing engine to clean, structure, and apply a schema to the data.
    *   **Parquet File Format:** Efficient, columnar output format for Silver layer data to optimize query performance.
    *   **AWS S3:** Serves as the **Silver Layer**, storing cleaned and partitioned Parquet files.
    *   **Apache Airflow:** Orchestrates the PySpark job, ensuring it runs after the ingestion task is complete.

### Phase 3: Business Aggregation (Silver to Gold)
*   **Objective:** Create business-centric, aggregated tables from the Silver layer data that are ready for analytics.
*   **Tech Stack & Roles:**
    *   **Apache Spark (PySpark):** Performs complex transformations and business logic (e.g., calculating moving averages, joining datasets).
    *   **AWS S3:** Serves as the **Gold Layer**, storing the final, aggregated datasets in Parquet format.
    *   **Apache Airflow:** Triggers this aggregation job after the Silver layer processing is complete.

### Phase 4: Data Warehousing and Modeling (dbt + Snowflake)
*   **Objective:** Load the aggregated data into a performant data warehouse and use dbt to create the final, trusted data models for analytics.
*   **Tech Stack & Roles:**
    *   **Snowflake:** The cloud data warehouse providing the high-performance query engine for BI.
    *   **dbt (Data Build Tool):** The transformation and modeling layer within Snowflake. Used to build, test, and document the final data marts.
    *   **Apache Airflow:** Orchestrates the final steps: loading data from S3 to Snowflake and then triggering a `dbt run`.

### Phase 5: Deployment and Analytics
*   **Objective:** Containerize the application, set up CI/CD, and connect BI tools for visualization.
*   **Tech Stack & Roles:**
    *   **Docker:** Creates containers for the application to ensure consistency across environments.
    *   **CI/CD (e.g., GitHub Actions):** Automates testing (`pytest`, `dbt test`) and deployment workflows.
    *   **BI Tools (e.g., Tableau, Power BI):** The final presentation layer for creating dashboards from the data in Snowflake.

---

*This document consolidates the project plan. It is recommended to deprecate other scattered planning files and use this as the single source of truth.*