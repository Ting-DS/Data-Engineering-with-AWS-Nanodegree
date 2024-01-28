# Data-Engineering-with-AWS
<div align="center">
  <img src="https://github.com/Ting-DS/Data-Engineering-with-AWS/blob/main/image/DE_AWS.png" width="80%">
</div>

## Introduction
This repository contains four Data Engineering projects created by [Ting Lu](https://www.linkedin.com/in/ting-lu-9949b0233/), using AWS to build ETL/ELT pipelines and conduct big data analysis to address various business requirements (link as follows):

 - [Data Modeling with Apache Cassandra](https://github.com/Ting-DS/Data-Engineering-with-AWS/tree/main/Data-Modeling-Cassandra): Build an ETL pipeline using Python driver from a directory of CSV files to an Apache Cassandra NoSQL database to improved efficiency in querying user activity data.

 - [Cloud Data Warehouse & ELT Pipeline](https://github.com/Ting-DS/Data-Engineering-with-AWS/tree/main/Cloud-Data-Warehouse):Build an ETL pipeline that extracts JSON logs and metadata from S3, loads them into AWS Redshift staging tables, and transforms the data into a Star Schema Database with dimensional tables for marketing and analytics teams to query song play insights.
   
 - [STEDI Human Balance Analytics- Data Lakehouse solution](https://github.com/Ting-DS/Data-Engineering-with-AWS/tree/main/Data-Lakehouse-Spark-AWS): Construct a lakehouse solution with landing, trusted, and curated data lake zones in AWS, utilizing Spark, Python, Glue Studio, S3, and Athena to address the STEDI data scientists' requirements.

 - [Automatic Data Pipeline with Apache Airflow](https://github.com/Ting-DS/Data-Engineering-with-AWS/tree/main/Airflow-Data-Pipeline): Design, automate and monitor ETL pipelines in Apache Airflow for processing JSON logs and metadata from AWS S3 into Redshift data warehouse, involving custom operators for staging, data loading, and data quality checks, to create versatile ETL pipelines with monitoring and backfill capabilities.

## Keywords & Reference: 

[Apache Airflow](https://airflow.apache.org/), [Apache Spark](https://spark.apache.org/),[Python](https://www.python.org/),[PostgreSQL](https://www.postgresql.org/), [Apache Cassandra](http://cassandra.apache.org/), [NoSQL](https://en.wikipedia.org/wiki/NoSQL), [Data Warehouse](https://en.wikipedia.org/wiki/Data_warehouse), [Data Lakehouse](https://databricks.com/solutions/lakehouse), [AWS S3](https://aws.amazon.com/s3/), [Redshift](https://aws.amazon.com/redshift/), [Athena](https://aws.amazon.com/athena/), [Glue Studio](https://aws.amazon.com/glue/),[Database](https://en.wikipedia.org/wiki/Database), [Schema](https://en.wikipedia.org/wiki/Database_schema), [ETL & ELT pipeline](https://en.wikipedia.org/wiki/ETL), [Data Modeling](https://en.wikipedia.org/wiki/Data_modeling), [Big Data](https://www.oracle.com/big-data/what-is-big-data/)

## Some example
#### Data Warehouse Schema in Redshift for Song Play Analysis

<div align="center">
  <img src="https://github.com/Ting-DS/Cloud-Data-Warehouse/blob/main/image/Schema.png" width="80%">
</div>

#### Data Lakehouse Solution for STEDI Human Balance Analytics
<div align="center">
  <img src="https://github.com/Ting-DS/Data-Lakehouse-Spark-AWS/blob/main/image/AWS_draw.png" width="100%">
</div>

#### Airflow DAG for for User Activities Analysis
<div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/dag-graph.png" width="100%">
</div>


