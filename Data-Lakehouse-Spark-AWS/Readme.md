# STEDI Human Balance Analytics- Data Lakehouse solution in AWS
# Introduction
The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:

 - trains the user to do a STEDI balance exercise;
 - has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
 - has a companion mobile app that collects customer data and interacts with the device sensors.
   
As a data engineer on the STEDI Step Trainer team, I'll extract the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS so that Data Scientists can train the ML model.


#### Using Spark, Python, [AWS Glue Studio](https://docs.aws.amazon.com/glue/latest/ug/what-is-glue-studio.html), [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) and [AWS Athena](https://aws.amazon.com/athena/), create Python scripts using [PySpark](https://spark.apache.org/docs/latest/api/python/index.html) and query [Glue Table](https://docs.aws.amazon.com/glue/latest/dg/tables-described.html) using SQL to build a lakehouse solution with landing-trusted-curated data lake zones in AWS that satisfies these requirements from the STEDI data scientists.

<div align="center">
  <img src="https://github.com/Ting-DS/Data-Lakehouse-Spark-AWS/blob/main/image/AWS_draw.png" width="100%">
</div>

STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them. Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance. The **Step Trainer** is just a motion sensor that records the distance of the object detected. The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions. The STEDI team wants to use the motion sensor data to train a machine learning model to **detect steps accurately in real-time**. **Privacy** will be a primary consideration in deciding what data can be used. Some of the early adopters have agreed to share their data for research purposes. Only these customers’ Step Trainer and **accelerometer data** should be used in the training data for the machine learning model.

# Data source

STEDI has **three JSON data** sources to use from the Step Trainer:

### 1. Customer Records (from fulfillment and the STEDI website)
AWS S3 Bucket URI - `s3://cd0030bucket/customers/`
``` 
 - serialnumber
 - sharewithpublicasofdate
 - birthday
 - registrationdate
 - sharewithresearchasofdate
 - customername
 - email
 - lastupdatedate
 - phone
 - sharewithfriendsasofdate
```
### 2. Step Trainer Records (data from the motion sensor):
AWS S3 Bucket URI - `s3://cd0030bucket/step_trainer/`
```
 - sensorReadingTime
 - serialNumber
 - distanceFromObject
```
### 3. Accelerometer Records (from the mobile app):
AWS S3 Bucket URI - `s3://cd0030bucket/accelerometer/`
```
 - timeStamp
 - user
 - x
 - y
 - z
```
# Data Lakehouse Architecture

## Customers Data [JSON / Parquet]
 - Landing Zone: store raw customer records data in AWS S3 landing zone. 
 - Trusted Zone: only store the customer records who agreed to share their data for research purposes. 
 - Curated Zone: only store customers who have accelerometer data and have agreed to share their data for research. 

## Accelerometer Data [JSON / Parquet]
 - Landing Zone: store raw accelerometer data in AWS S3 landing zone.
 - Trusted Zone: only store accelerometer readings from customers who agreed to share their data for research purposes.
## Step Trainer Data [JSON / Parquet]
 - Landing Zone: store raw Step Trainer data in AWS S3 landing zone.
 - Trusted Zone: store the Step Trainer Records data for customers who have accelerometer data and have agreed to share their data for research (customers curated zone).
## Machine Learning Data [JSON / Parquet]
 - Curated Zone: aggregated table that has each of the Step Trainer Readings, and the associated accelerometer reading data for the same timestamp, but only for customers who have agreed to share their data.
 
# AWS configuration (using AWS cloud shell)
 - Create S3 bucket
 - Configure [S3 VPC Gateway Endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
 - Create [Glue IAM Service role](https://docs.aws.amazon.com/glue/latest/dg/set-up-iam.html)
 - Grant S3Access privileges to Glue
 - Give Glue access to data in special S3 buckets used for Glue configuration and other resources
 - Copy raw data from S3 data source into your S3 bucket. Ex.
 `aws s3 cp ./project/starter/step_trainer s3://stedi-lake-house/step_trained/landing/ --recursive`
 
# Data quality problem solution

In the original Customer Data, the **serial number** should serve as a unique identifier for the STEDI Step Trainer. Each customer's purchase of a STEDI Step Trainer should have a distinct serial number. However, due to a defect in the fulfillment website, the same set of 30 serial numbers was repeatedly used for millions of customers. This problem resulted in a significant confusion: we are unable to determine which customer owns which STEDI Step Trainer.

To address this issue for the Data Science team:

 - Cleaning Customer Data: Cleaning Customer data from the Trusted Zone, including only those customers who have accelerometer data and have agreed to share their data for research. This cleaning process will create a Glue table named "customers_curated."

 - Creating Two Glue Studio Jobs: These two jobs aim to read the Step Trainer IoT data stream, populate a Trusted Zone Glue table named "step_trainer_trusted" containing accelerometer data and STEDI Step Trainer records data from customers who have agreed to share their data. Additionally, an aggregated table will be created that associates each Step Trainer Reading with the corresponding timestamp's accelerometer reading data, but only for customers who have consented to share their data. This aggregated table will be named "machine_learning_curated."

# AWS Glue Catalog & Glue Table DDL
```
CREATE EXTERNAL TABLE `machine_learning_curated`(
  `serialnumber` string COMMENT 'from deserializer', 
  `sharewithresearchasofdate` bigint COMMENT 'from deserializer', 
  `registrationdate` bigint COMMENT 'from deserializer', 
  `customername` string COMMENT 'from deserializer', 
  `sensorreadingtime` bigint COMMENT 'from deserializer', 
  `distancefromobject` int COMMENT 'from deserializer', 
  `lastupdatedate` bigint COMMENT 'from deserializer', 
  `timestamp` bigint COMMENT 'from deserializer', 
  `user` string COMMENT 'from deserializer', 
  `x` double COMMENT 'from deserializer', 
  `y` double COMMENT 'from deserializer', 
  `z` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
WITH SERDEPROPERTIES ( 
  'case.insensitive'='TRUE', 
  'dots.in.keys'='FALSE', 
  'ignore.malformed.json'='FALSE', 
  'mapping'='TRUE') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://stedi-lake-house/ml'
TBLPROPERTIES (
  'classification'='json', 
  'transient_lastDdlTime'='1695438973')
```
 
# AWS Glue Studio

<div align="center">
  <img src="https://github.com/Ting-DS/Data-Lakehouse-Spark-AWS/blob/main/image/Glue.png" width="100%">
</div>

# AWS Athena

<div align="center">
  <img src="https://github.com/Ting-DS/Data-Lakehouse-Spark-AWS/blob/main/image/Athena.png" width="100%">
</div>

<div align="center">
  <img src="https://github.com/Ting-DS/Data-Lakehouse-Spark-AWS/blob/main/AthenaSQLQuery/machine_learning_curated.png" width="100%">
</div>

# Reference:

 - [Data Engineering with AWS](https://www.amazon.com/Data-Engineering-AWS-Gareth-Eagar/dp/1800560419)
 - [Data Lakehouse](https://aws.amazon.com/blogs/architecture/use-a-reusable-etl-framework-in-your-aws-lake-house-architecture/)
 - [AWS Glue Studio](https://docs.aws.amazon.com/glue/latest/ug/what-is-glue-studio.html)
 - [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
 - [AWS Athena](https://aws.amazon.com/athena/)
 - [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
 - [Glue Table](https://docs.aws.amazon.com/glue/latest/dg/tables-described.html) 


