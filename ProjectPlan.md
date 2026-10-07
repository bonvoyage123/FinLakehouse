# FinLakehouse --- Financial Markets Data Engineering Platform

## 1. Project Overview

**Project:** FinLakehouse\
**Type:** Portfolio-grade Data Engineering project\
**Primary objective:** Build a production-style financial markets data
platform that ingests market and company financial data with Python,
stores raw and curated data in AWS S3, processes Raw through Bronze and
Silver with PySpark jobs on AWS Glue, loads Silver data into Snowflake,
creates analytical models there with dbt, orchestrates the pipeline
with Airflow on AWS MWAA, and exposes the resulting datasets through a
Power BI dashboard.

The project is designed primarily as a **Data Engineering project**,
with the dashboard serving as the consumer of the platform.

### Core pipeline

``` text
Financial Modeling Prep API
        |
        v
Python Ingestion
        |
        v
AWS S3 - Raw
        |
        v
AWS Glue (PySpark)
        |
        v
AWS S3 - Bronze -> Silver
        |
        v
Snowflake - Silver data
        |
        v
dbt in Snowflake
        |
        v
Gold / Analytical Marts in Snowflake
        |
        v
    Power BI

Airflow on AWS MWAA orchestrates ingestion, Glue, Snowflake and dbt.
```

------------------------------------------------------------------------

## 2. Business Problem

Build a production-style Financial Lakehouse that:

-   Ingests stock-market and company financial data.
-   Preserves raw source data.
-   Processes data using a Medallion-style architecture.
-   Performs data cleansing and quality validation.
-   Supports incremental processing.
-   Models business-ready analytical datasets.
-   Loads curated data into Snowflake.
-   Orchestrates the complete workflow using Airflow on AWS MWAA.
-   Provides business-facing analytics through Power BI.
-   Demonstrates software engineering, testing, CI/CD, logging, and
    documentation practices.

The project should resemble a real data platform rather than a simple
ETL tutorial.

------------------------------------------------------------------------

## 3. Project Goals

### Primary goals

1.  Demonstrate practical PySpark data engineering with AWS Glue.
2.  Demonstrate AWS S3 data-lake fundamentals.
3.  Demonstrate Snowflake ingestion, modelling, and analytical
    workloads.
4.  Demonstrate dbt-based transformation and testing.
5.  Demonstrate Airflow orchestration on AWS MWAA.
6.  Demonstrate incremental and idempotent data processing.
7.  Demonstrate data-quality engineering.
8.  Demonstrate Python application/package structure.
9.  Demonstrate Docker and GitHub Actions.
10. Produce a professional GitHub portfolio project that can be defended
    during interviews.

### Learning philosophy

The project will follow:

> **Build → encounter a problem → learn the required concept → implement
> → test → document.**

The objective is not to learn every technology exhaustively before
building the project.

------------------------------------------------------------------------

# 4. Project Scope

## 4.1 Initial data domain

The first version will focus on:

-   Equities
-   Market indices
-   Company information
-   Company financial statements

Future domains such as derivatives, FX, commodities, and real-time
market data are explicitly outside the initial scope.

------------------------------------------------------------------------

## 4.2 Initial datasets

### Dataset 1 --- Daily Stock Prices

``` text
instrument_id
ticker
trade_date
open
high
low
close
adjusted_close
volume
```

### Dataset 2 --- Company Profile

``` text
company_id
ticker
company_name
sector
industry
country
currency
market_cap
```

### Dataset 3 --- Financial Statements

``` text
company_id
report_date
fiscal_year
revenue
operating_income
net_income
assets
liabilities
cash
debt
eps
```

### Dataset 4 --- Corporate Actions

To be introduced after the initial pipeline is working.

``` text
instrument_id
effective_date
action_type
ratio
cash_amount
```

Examples:

-   Dividend
-   Stock split
-   Bonus

------------------------------------------------------------------------

# 5. Data Sources

The original project plan identified the following possible sources:

-   Yahoo Finance
-   Alpha Vantage
-   Financial Modeling Prep

The initial implementation will use **one market-data API**.

Additional sources should only be introduced after the first end-to-end
pipeline is stable.

------------------------------------------------------------------------

# 6. Architecture

## 6.1 Logical architecture

``` text
             Financial Modeling Prep API
                           |
                           v
                    Python Ingestion
                           |
                           v
                       S3 Raw
                           |
                           v
              AWS Glue (PySpark jobs)
                Raw -> Bronze -> Silver
                           |
                           v
                       S3 Silver
                           |
                           v
                      Snowflake
                    Silver data layer
                           |
                           v
                 dbt in Snowflake
                  Gold / marts
                           |
                           v
                       Power BI

          Airflow on AWS MWAA orchestrates:
       Python ingestion -> Glue -> Snowflake -> dbt
```

------------------------------------------------------------------------

# 7. Medallion Architecture

## 7.1 Raw / Landing

Purpose:

> Preserve exactly what was received from the source.

Characteristics:

-   Immutable where practical.
-   Raw API responses.
-   Source metadata.
-   Ingestion timestamp.
-   Partitioned by ingestion date.
-   No business transformations.

Example:

``` text
s3://finlakehouse/raw/
    market_prices/
        year=2026/month=10/day=01/
    company_profiles/
        year=2026/month=10/day=01/
    financial_statements/
        year=2026/month=10/day=01/
```

------------------------------------------------------------------------

## 7.2 Bronze

Purpose:

> Convert raw API responses into structured, queryable data.

Responsibilities:

-   Read raw JSON.
-   Apply an explicit schema where practical.
-   Standardize data types.
-   Handle malformed records.
-   Convert to Parquet.
-   Partition data appropriately.
-   Run as an AWS Glue PySpark job reading S3 Raw and writing S3
    Bronze.

Example:

``` text
s3://finlakehouse/bronze/
    stock_prices/
    company_profiles/
    financial_statements/
```

------------------------------------------------------------------------

## 7.3 Silver

Purpose:

> Produce clean, trusted, standardized datasets.

Responsibilities:

-   Remove duplicates.
-   Handle null values.
-   Standardize dates and timestamps.
-   Normalize currencies where required.
-   Generate stable identifiers.
-   Apply business rules.
-   Perform data-quality checks.
-   Handle late-arriving or corrected records.
-   Run as an AWS Glue PySpark job reading Bronze and writing trusted
    Silver data to S3.

Example datasets:

``` text
stock_prices
companies
financials
dividends
splits
```

------------------------------------------------------------------------

## 7.4 Gold

Purpose:

> Produce business-ready analytical datasets.

Gold transformations will primarily be implemented using dbt in
Snowflake.

Example models:

``` text
dim_company
dim_date
fact_stock_prices
fact_financials
mart_daily_stock_summary
mart_company_financials
mart_sector_performance
mart_market_performance
```

------------------------------------------------------------------------

# 8. Data Engineering Requirements

## 8.1 Incremental processing

The pipeline must avoid reprocessing the complete historical dataset for
every run.

The implementation should support:

-   New daily data.
-   Reprocessing of a specific date.
-   Duplicate delivery.
-   Late-arriving data.
-   Corrected source records.

------------------------------------------------------------------------

## 8.2 Idempotency

Running the same pipeline multiple times for the same input should not
create duplicate business records.

Example business key:

``` text
(ticker, trade_date)
```

for daily stock prices.

------------------------------------------------------------------------

## 8.3 Data quality

Initial checks should include:

-   No duplicate `(ticker, trade_date)` records.
-   No negative trading volume.
-   `high >= low`.
-   `open` is within the day's high/low range.
-   `close` is within the day's high/low range.
-   Required fields are not null.
-   Data freshness check.
-   Valid date values.
-   Valid instrument identifiers.

Data-quality failures should be visible in logs and should prevent
invalid data from silently reaching downstream analytical models.

------------------------------------------------------------------------

# 9. Technology Responsibilities

  Technology       Primary responsibility
  ---------------- -------------------------------------------------
  Python           Financial API ingestion, utilities, application structure
  AWS S3           Raw, Bronze and Silver data storage
  AWS Glue         Managed execution of PySpark Raw-to-Silver jobs
  IAM              AWS access control for S3, Glue and MWAA
  PySpark          Bronze/Silver transformations and validation in Glue
  Parquet          Columnar Bronze/Silver lake storage
  Snowflake        Silver data and analytical warehouse
  dbt              Snowflake SQL transformations, Gold models and tests
  Airflow / MWAA   End-to-end pipeline orchestration on AWS
  Docker           Reproducible local development and testing
  GitHub Actions   CI/CD
  Power BI         Business-facing analytics from Snowflake Gold models

------------------------------------------------------------------------

# 10. PySpark Focus

PySpark running as AWS Glue jobs is the primary technical focus of the
project. Glue owns the Raw-to-Bronze and Bronze-to-Silver processing
steps; Python ingestion remains a separate step that lands API responses
in S3 Raw.

The implementation should demonstrate:

-   DataFrame operations.
-   Spark SQL.
-   Joins.
-   Aggregations.
-   Window functions.
-   Deduplication.
-   Partitioning.
-   Repartitioning and coalescing.
-   Broadcast joins.
-   Handling data skew.
-   Predicate pushdown.
-   Parquet.
-   Explain plans.
-   Basic performance optimisation.

The project should contain enough realistic data-processing work that
PySpark can be discussed as a substantive skill during interviews.

------------------------------------------------------------------------

# 11. Snowflake Scope

Snowflake should be used for the analytical warehouse and dbt modelling
layers. Curated Silver data is loaded from S3 into Snowflake before dbt
builds Gold models.

The project should cover:

-   Databases.
-   Schemas.
-   Tables.
-   Stages and storage integrations for S3 Silver data.
-   File formats.
-   Loading Silver Parquet data.
-   `COPY INTO`.
-   Incremental loading.
-   Warehouse usage.
-   Query performance concepts.
-   Micro-partitions.
-   Clustering concepts.
-   Basic access control.

The project should prioritize practical understanding of features
actually used in the implementation.

------------------------------------------------------------------------

# 12. dbt Scope

dbt will own the analytical transformation layer.

Expected functionality:

-   Sources.
-   Staging models.
-   Core models.
-   Gold models.
-   Incremental models.
-   Tests.
-   Macros.
-   Documentation.
-   Snapshots where useful.
-   Model dependencies and lineage.

Example:

``` text
raw / core Snowflake tables
            |
            v
       stg_prices
            |
            v
    int_daily_prices
            |
            v
     fct_daily_prices
            |
            v
mart_instrument_performance
```

------------------------------------------------------------------------

# 13. Airflow Scope

Apache Airflow, deployed on AWS Managed Workflows for Apache Airflow
(MWAA), will orchestrate the complete workflow after the individual
components are independently functional.

Target DAG:

``` text
ingest_api
    |
    v
glue_transform
    |
    v
load_snowflake
    |
    v
dbt_run
    |
    v
data_quality
```

Airflow functionality:

-   Scheduling.
-   Task dependencies.
-   Retries.
-   Retry delays.
-   Logging.
-   Failure handling.
-   Parameterisation.
-   Backfills.
-   Catchup.
-   Idempotent task design.
-   AWS Glue job submission and completion monitoring.
-   MWAA deployment and AWS connection/IAM configuration.

------------------------------------------------------------------------

# 14. Dashboard

A single Power BI dashboard will be built with three logical pages.

## Page 1 --- Market Overview

-   Market indices.
-   Top gainers.
-   Top losers.
-   Trading volume.
-   Sector performance.
-   Market trends.

## Page 2 --- Company Analysis

-   Price history.
-   30-day moving average.
-   200-day moving average.
-   Revenue.
-   Net income.
-   EPS.
-   P/E.
-   P/B.
-   ROE.
-   Debt/Equity.

## Page 3 --- Pipeline Health

-   Last successful ingestion.
-   Records ingested.
-   Records rejected.
-   Data-quality failures.
-   Pipeline duration.
-   Pipeline status.

The dashboard is a consumer of the data platform, not the primary
purpose of the project.

------------------------------------------------------------------------

# 15. Project Phases

## Phase 0 --- Project Planning

**Duration:** 2 days

### Objectives

-   Finalize architecture.
-   Select initial API.
-   Finalize datasets.
-   Create GitHub repository.
-   Create repository structure.
-   Set up Python environment.
-   Set up Docker.
-   Plan AWS S3, Glue, IAM, Snowflake and MWAA configuration.
-   Define backlog.

### Deliverables

-   GitHub repository.
-   Initial README.
-   Architecture diagram.
-   Project specification.
-   Docker environment.
-   Development roadmap.

### Exit criteria

Repository is ready for development.

------------------------------------------------------------------------

## Phase 1 --- Python Data Ingestion

**Target:** Week 1

### Objectives

Build the initial ingestion framework.

### Tasks

-   Create API client.
-   Handle authentication.
-   Implement timeout handling.
-   Implement retry logic.
-   Add logging.
-   Add ingestion metadata.
-   Store raw API responses.
-   Partition data by ingestion date.
-   Upload data to S3.

### Deliverables

-   Python ingestion package.
-   Raw JSON samples.
-   S3 landing zone.
-   Logging.

### Exit criteria

Daily market data can be successfully retrieved and landed in S3.

------------------------------------------------------------------------

## Phase 2 --- AWS Glue Bronze Layer

**Target:** Week 2

### Objectives

Create the first AWS Glue PySpark job to convert raw API data in S3 into
structured Bronze Parquet data.

### Tasks

-   Read raw JSON.
-   Create the Glue job and configure its IAM role and S3 access.
-   Define/validate schema.
-   Standardize data types.
-   Handle malformed records.
-   Write Parquet.
-   Partition datasets.
-   Validate output.

### Deliverables

-   Bronze datasets.
-   Partitioned Parquet.
-   AWS Glue PySpark job for Raw-to-Bronze processing.

### Exit criteria

Raw data is converted into queryable Bronze datasets in S3 by AWS Glue.

------------------------------------------------------------------------

## Phase 3 --- AWS Glue Silver Layer

**Target:** Week 3

### Objectives

Produce trusted, clean datasets.

### Tasks

-   Deduplication.
-   Null handling.
-   Date/timestamp standardization.
-   Currency normalization where required.
-   Primary/business-key generation.
-   Business-rule validation.
-   Data-quality reporting.
-   Incremental processing.
-   Idempotency.
-   Late-arriving/corrected data handling.
-   Write curated Silver Parquet datasets to S3.

### Deliverables

-   Clean stock prices.
-   Company master.
-   Financial statements.
-   Data-quality reports.

### Exit criteria

Trusted Silver datasets are available in S3 and are produced by AWS Glue.

------------------------------------------------------------------------

## Phase 4 --- Snowflake and dbt Gold Layer

**Target:** Weeks 4--5

### Objectives

Create business-ready analytical models.

### Tasks

-   Configure Snowflake.
-   Create schemas.
-   Create stages/file formats.
-   Configure secure Snowflake access to S3 Silver data.
-   Load Silver data into Snowflake staging/core tables.
-   Build dbt sources.
-   Build staging models.
-   Build dimensions.
-   Build fact tables.
-   Build analytical marts.
-   Add dbt tests.
-   Add incremental models.
-   Document models.

### Deliverables

-   Snowflake warehouse layer.
-   dbt project.
-   DimCompany.
-   DimDate.
-   FactStockPrices.
-   FactFinancials.
-   Analytical marts.
-   dbt tests and documentation.

### Exit criteria

Gold datasets are ready for BI consumption.

------------------------------------------------------------------------

## Phase 5 --- Airflow on AWS MWAA Orchestration

**Target:** Week 6

### Objectives

Automate the end-to-end pipeline.

### Tasks

-   Deploy/configure the MWAA environment, IAM permissions and required
    connections.
-   Create the Airflow DAG and deploy it to MWAA.
-   Implement the task chain: `ingest_api` → `glue_transform` →
    `load_snowflake` → `dbt_run` → `data_quality`.
-   Have `ingest_api` fetch financial API data and land it in S3 Raw.
-   Have `glue_transform` submit and monitor the AWS Glue job that
    produces Bronze and Silver data.
-   Have `load_snowflake` load S3 Silver data into Snowflake.
-   Have `dbt_run` build and test the dbt models.
-   Have `data_quality` run final pipeline data-quality checks.
-   Add retries.
-   Add logging.
-   Add failure handling.
-   Add scheduling.
-   Test backfills and reruns.

### Deliverables

-   End-to-end Airflow DAG running on AWS MWAA.
-   Glue job monitoring and Snowflake/dbt orchestration.
-   Pipeline logs.
-   Retry/failure handling.

### Exit criteria

The complete pipeline can be executed through Airflow on AWS MWAA.

------------------------------------------------------------------------

## Phase 6 --- Dashboard

**Target:** Week 6--7

### Objectives

Expose Gold datasets to business users.

### Tasks

-   Connect Power BI to Snowflake.
-   Build market overview.
-   Build company analysis.
-   Build pipeline-health view.
-   Validate dashboard calculations.

### Deliverables

-   Power BI dashboard.
-   Screenshots for GitHub.
-   Dashboard documentation.

### Exit criteria

Users can consume the curated data through an interactive dashboard.

------------------------------------------------------------------------

## Phase 7 --- Production Engineering

**Target:** Week 7

### Objectives

Improve engineering quality.

### Tasks

-   Dockerize services.
-   Add unit tests.
-   Add configuration management.
-   Use environment variables/secrets.
-   Add structured logging.
-   Add error handling.
-   Add GitHub Actions.
-   Add linting.
-   Add automated tests.
-   Add security checks where practical.

### Potential tooling

-   pytest
-   Ruff/flake8
-   Bandit
-   Safety
-   Trivy
-   GitHub Actions

### Exit criteria

The project can be validated automatically through CI/CD.

------------------------------------------------------------------------

## Phase 8 --- Documentation and Portfolio Polish

**Target:** Week 8

### Objectives

Prepare the project for interviews and GitHub.

### Deliverables

-   Architecture diagram.
-   Data-flow diagram.
-   Sequence diagram.
-   ER diagram.
-   Data lineage.
-   README.
-   Setup instructions.
-   Screenshots.
-   Sample data-quality report.
-   CI/CD documentation.
-   Demo video.
-   Interview question bank.
-   Design decisions document.
-   Future-enhancement roadmap.

### Exit criteria

Project is portfolio-ready and can be demonstrated end-to-end.

------------------------------------------------------------------------

# 16. Proposed Repository Structure

``` text
finlakehouse/
│
├── airflow/
│   ├── dags/
│   └── plugins/
│
├── glue/
│   └── jobs/
│       ├── raw_to_bronze.py
│       └── bronze_to_silver.py
│
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   ├── utilities/
│   └── config/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── core/
│   │   └── marts/
│   ├── macros/
│   ├── snapshots/
│   └── tests/
│
├── tests/
│
├── docker/
│
├── dashboards/
│
├── docs/
│   ├── architecture/
│   ├── data-model/
│   ├── decisions/
│   └── interview-notes/
│
├── notebooks/
│
├── data/
│   ├── sample/
│   └── test/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── ProjectPlan.md
```

------------------------------------------------------------------------

# 17. Design Decisions to Document

Create a `docs/decisions/` directory and record important decisions.

Examples:

### Why S3?

-   Durable object storage.
-   Separation of storage and compute.
-   Suitable for raw and curated data.

### Why Parquet?

-   Columnar format.
-   Compression.
-   Efficient analytical processing.
-   Schema support.

### Why PySpark?

-   Distributed processing.
-   Suitable for large-scale transformation.
-   Provides opportunities to demonstrate Spark optimisation.
-   Reusable transformation logic can be developed and tested locally,
    then packaged for Glue job deployment.

### Why AWS Glue?

-   Managed, serverless execution for PySpark ETL jobs.
-   Integrates with S3 and the AWS data platform.
-   Provides job monitoring and operational integration with MWAA.

### Why Snowflake?

-   Analytical warehouse.
-   Separation of compute and storage.
-   SQL-based analytical workloads.

### Why dbt?

-   SQL transformation framework.
-   Testing.
-   Documentation.
-   Lineage.
-   Incremental modelling.

### Why Airflow?

-   Workflow orchestration.
-   Scheduling.
-   Dependencies.
-   Retry and failure handling.
-   AWS MWAA provides a managed Airflow environment for the deployed
    pipeline.

------------------------------------------------------------------------

# 18. Testing Strategy

## Unit tests

Test:

-   API client.
-   Transformation functions.
-   Validation functions.
-   Utility functions.

## Data-quality tests

Test:

-   Uniqueness.
-   Nullability.
-   Valid ranges.
-   Referential integrity.
-   Freshness.
-   Business rules.

## Integration tests

Test:

``` text
API → Python → S3 Raw
S3 Raw → AWS Glue PySpark → S3 Bronze → S3 Silver
S3 Silver → Snowflake
Snowflake → dbt
Snowflake Gold → Power BI
```

## Pipeline tests

Test:

-   Successful execution.
-   Retry behaviour.
-   Failure handling.
-   Rerun/idempotency.
-   Backfill.

------------------------------------------------------------------------

# 19. CI/CD

GitHub Actions should perform at least:

``` text
Pull Request
      |
      v
Lint
      |
      v
Unit Tests
      |
      v
Data/SQL Tests
      |
      v
Security Checks
      |
      v
Build / Validation
```

The objective is to demonstrate an automated engineering workflow rather
than simply storing code on GitHub.

------------------------------------------------------------------------

# 20. Interview Preparation

The completed project should generate an interview question bank.

## PySpark

-   Why Spark instead of Pandas?
-   How do AWS Glue jobs read from and write to S3?
-   How do you monitor and retry a failed Glue job?
-   What causes a shuffle?
-   When would you use a broadcast join?
-   How would you handle data skew?
-   How does partitioning affect performance?
-   What does lazy evaluation mean?
-   How would you troubleshoot a slow Spark job?

## S3

-   Why S3?
-   How would you partition the data?
-   How would you secure the bucket?
-   What happens if the same file arrives twice?

## Snowflake

-   What is a micro-partition?
-   How does partition pruning work?
-   When would you use clustering?
-   How would you troubleshoot a slow query?
-   How would you perform incremental loading?

## dbt

-   What is an incremental model?
-   What are sources?
-   How do dbt tests work?
-   What are snapshots?
-   How do you handle changing source schemas?

## Airflow

-   What does AWS MWAA manage compared with self-hosted Airflow?
-   How does a DAG submit and monitor an AWS Glue job?
-   How are AWS credentials and permissions provided to MWAA tasks?
-   What happens when a task fails?
-   How do retries work?
-   What is catchup?
-   What is a backfill?
-   How do you make a DAG idempotent?
-   How would you handle a failed downstream task?

## Architecture

-   Why this architecture?
-   What happens if the API is unavailable?
-   What happens if the schema changes?
-   What happens if data arrives late?
-   What happens if the pipeline runs twice?
-   How would you scale the platform?
-   What would you change if data volume increased from GBs to TBs?

------------------------------------------------------------------------

# 21. Scope Control

The following are **not required for V1**:

-   Kafka.
-   Real-time market analytics.
-   RAG.
-   Portfolio optimization.
-   Complex ML models.
-   Multiple market-data APIs.
-   Terraform.
-   Apache Iceberg.
-   Great Expectations.

These are potential future enhancements only.

------------------------------------------------------------------------

# 22. Future Enhancements

Once V1 is stable, potential extensions include:

1.  Great Expectations.
2.  Apache Iceberg.
3.  Kafka/streaming.
4.  Terraform.
5.  Cost monitoring.
6.  RAG over financial reports.
7.  Portfolio analytics.
8.  Real-time market analytics.
9.  Additional financial-data sources.
10. Multi-market support.

------------------------------------------------------------------------

# 23. Definition of Done

The project is considered complete when:

-   [ ] Market data can be ingested from an API.
-   [ ] Raw data is preserved in S3.
-   [ ] Bronze data is available in Parquet.
-   [ ] Silver data is cleaned and validated.
-   [ ] AWS Glue processes S3 Raw into Bronze and Silver.
-   [ ] Incremental processing works.
-   [ ] Duplicate ingestion does not create duplicate business records.
-   [ ] Late/corrected data has a defined handling strategy.
-   [ ] Silver data is loaded into Snowflake.
-   [ ] dbt creates Gold models.
-   [ ] dbt tests are implemented.
-   [ ] Airflow on AWS MWAA orchestrates ingestion, Glue, Snowflake and
    dbt.
-   [ ] Retries and failure handling work.
-   [ ] Power BI consumes Gold data.
-   [ ] Unit tests exist.
-   [ ] CI/CD runs automatically.
-   [ ] Docker environment is documented.
-   [ ] Architecture documentation is complete.
-   [ ] Data lineage is documented.
-   [ ] Repository is clean and professional.
-   [ ] Interview questions and design decisions are documented.

------------------------------------------------------------------------

# 24. Final Project Positioning

The project should be presented as:

> **FinLakehouse --- an end-to-end financial markets data engineering
> platform demonstrating Python, PySpark on AWS Glue, S3, Snowflake, dbt,
> Airflow on MWAA, data quality, incremental processing, Docker and CI/CD.**

The project is intended to demonstrate the ability to design, build,
operate, troubleshoot, and explain a modern data pipeline --- not simply
to demonstrate familiarity with individual technologies.
