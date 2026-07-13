# 🌊 Data Lake API Ingestion Pipeline 

## Overview
An end-to-end Extract, Load, Transform (ELT) data pipeline designed to ingest live streaming data from external REST APIs. This project demonstrates modern Big Data storage principles by transforming nested JSON payloads into highly optimized, columnar Parquet files, preparing the data for scalable Cloud Warehouse analytics.

## The Business Problem
Traditional CSV storage is too slow and expensive for querying terabytes of analytical data. Modern data teams require pipelines that can hit third-party APIs, validate the schema, and store the output in compressed, columnar formats like Parquet to drastically reduce cloud storage costs and accelerate query performance in tools like Snowflake, AWS Athena, or Databricks.

## Architecture & Tech Stack
* **Extraction:** Python `requests` library for robust REST API interaction and payload retrieval.
* **Transformation:** `Pandas` for flattening nested JSON structures and enforcing strict data typing.
* **Storage Tier:** `PyArrow` serialization to write partitioned `.parquet` files, simulating a Bronze/Silver Data Lake architecture (e.g., AWS S3).

## Deployment Instructions
1. Install localized environments: `pip install -r requirements.txt`.
2. Execute the ingestion script: `python src/ingestion.py`.
3. The pipeline will query the live API and automatically generate the `/data_lake/silver/` directory, saving the compressed Parquet outputs locally.
