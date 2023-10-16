# Airflow-Data-Pipeline & AWS

<div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/AirflowAWS.jpeg" width="60%">
</div>

## Introduction
Sparkify is a music streaming company, aims to enhance automation and monitoring in their **data warehouse ETL** (Extract, Transform, Load) pipelines. They've chosen [Apache Airflow](https://airflow.apache.org/) as the tool for this purpose. I create advanced data pipelines with dynamic, reusable tasks, monitoring capabilities, and support for easy backfills. Additionally, ensuring **data quality** is crucial, so plan to run tests on their datasets post-ETL to detect any discrepancies. The source data is stored in [AWS S3](https://aws.amazon.com/pm/serv-s3/?trk=fecf68c9-3874-4ae2-a7ed-72b6d19c8034&sc_channel=ps&ef_id=EAIaIQobChMIiqPSj8TJgQMV-yezAB0VAwcmEAAYAiAAEgL8MPD_BwE:G:s&s_kwcid=AL!4422!3!536452728638!e!!g!!aws%20s3!11204620052!112938567994) and must be processed in Sparkify's [Amazon Redshift Serverless](https://aws.amazon.com/redshift/redshift-serverless/) data warehouse. The source datasets include **JSON logs detailing user activity and JSON metadata about the songs users listen to**. As a data engineer, I will create custom operators to perform tasks such as staging the data, filling the data warehouse, and running checks on the data quality as the final step.

## Project Airflow DAG 

<div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/dag-graph.png" width="100%">
</div>

<div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/DAG_grid.png" width="100%">
</div>


## Instuction
 - Create IAM user in AWS and Configure Redshift Serverless and S3 bucket (Note: same region).
   ```
    IAM Access Key: ''
    IAM secret access key: ''
    Redshift Cluster Endpoint: ''
   ```
 - Connect Airflow to AWS Redshift by [Airflow Web-UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html) configuration and Hooks such as [PostgresHook](https://airflow.apache.org/docs/apache-airflow/1.10.10/_api/airflow/hooks/postgres_hook/index.html).
 - Make sure the path is correct in your airflow workspace, run the following commands in the 
terminals to access the Airflow UI:
   ```
   /opt/airflow/start-services.sh
   /opt/airflow/start.sh
   airflow users create --email student@example.com --firstname aStudent --lastname aStudent --        password admin --role Admin --username admin
   airflow scheduler
   ```
   Wait for below:

   <div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/terminals.png" width="80%">
   </div>

 - Copy and load the Data Source into AWS S3
   ```
   aws s3 mb s3://sparkify-airflow/
   aws s3 cp s3://udacity-dend/log-data/ ~/log-data/ --recursive
   aws s3 cp s3://udacity-dend/song-data/ ~/song-data/ --recursive
   aws s3 cp ~/log-data/ s3://sparkify-airflow/log-data/ --recursive
   aws s3 cp ~/song-data/ s3://sparkify-airflow/song-data/ --recursive
   aws s3 ls s3://sparkify-airflow/log-data/
   aws s3 ls s3://sparkify-airflow/song-data/
   ```
 - Configuring the DAG in the [Airflow_DAG.py](https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/dags/Airflow_Pipeline_DAG.py):
   ```
   default_args = {
    'owner': 'Your Name',
    'depends_on_past': False,
    'start_date': datetime(2018, 11, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
    }
    
    @dag(
        default_args=default_args,
        description='Load and transform data in Redshift with Airflow',
        end_date=datetime(2018, 11, 2),
        schedule_interval='@hourly'
    )
   ```
## Build plugins operators:
#### [Stage to Redshift Operator](https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/pluginsOperators/stage_redshift.py):
The stage operator loads JSON files from S3 to Redshift using SQL COPY statements. It's templated to support timestamped file loading and backfills.

#### [Fact](https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/pluginsOperators/load_fact.py) and [Dimension Operators](https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/pluginsOperators/load_dimension.py):
These operators use SQL statements for data transformations, specifying the target database. Dimension operators support truncate-insert or insert modes, while fact operators are typically append-only.

#### [Data Quality Operator](https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/pluginsOperators/data_quality.py):
This operator runs SQL-based data checks, comparing actual results to expected outcomes. It raises exceptions for mismatches, triggering retries until task failure. For example, it can check for NULL values in columns and ensure data quality.

#### Note: Make sure to run the create_tables.py to create initial [star schema](https://awsonlinetraining.home.blog/2020/01/27/optimizing-for-star-schemas-on-amazon-redshift/) in Redshift data warehouse before execute the airflow_DAG.py to trigger the ETL pipeline and insert the data!

## Airflow DAGs monitoring

<div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/DAG_run.png" width="100%">
</div>

## Run SQL query in AWS Redshift to analyze the data
<div align="center">
  <img src="https://github.com/Ting-DS/Airflow-Data-Pipeline/blob/main/image/Redshift_SQL.png" width="100%">
</div>

## Reference

 - [Apache Airflow](https://airflow.apache.org/)
 - [Data Engineering with AWS](https://www.amazon.com/Data-Engineering-AWS-Gareth-Eagar/dp/1800560419)
 - [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
 - [Amazon Redshift Serverless](https://aws.amazon.com/redshift/redshift-serverless/)
 - [PostgresHook](https://airflow.apache.org/docs/apache-airflow/1.10.10/_api/airflow/hooks/postgres_hook/index.html)
