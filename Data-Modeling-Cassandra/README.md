# Data-Modeling-with-Apache-Cassandra

## Project Description
Sparkify is a startup in the music streaming industry, aims to analyze the data they have collected regarding songs and user activity on their new music streaming app. The data science team is particularly interested in understanding **what songs users are listening to**. Currently, they face difficulties in querying the data effectively since it is stored in a directory of CSV files, capturing user activity on the app.

The objective of this project is to create an **[Apache Cassandra](http://cassandra.apache.org/) NoSQL database** capable of answering queries about user activity data. The project will leverage data modeling with Apache Cassandra and complete an **ETL pipeline using Python driver**.

- <div align="center">
  <img src="https://github.com/Ting-DS/Data-Modeling-with-Apache-Cassandra/blob/main/images/apache-cassandra-logo.png" width="100%">
</div>

## Why use NoSQL rather than a relational SQL database?
Streaming data in a music app is often on a massive scale, reaching into the **terabytes** of data. Handling such large datasets becomes challenging when relying on a single machine due to the inherent scalability constraints of relational databases. Therefore, if your needs include **distributed** tables and **high-speed data retrieval** without the hindrance of ACID transactions or concerns about high availability, then NoSQL is the ideal choice. In our specific scenario, we've opted for Apache Cassandra as our AP fault-tolerant system, placing a premium on both availability and partition tolerance.

## File Overview & [CQL](https://cassandra.apache.org/doc/latest/cassandra/cql/) Process

- `event_data/` - contains 30-days web event data for user sessions in the streaming app in csv format. files are partitioned by day.
<div align="center">
  <img src="https://github.com/Ting-DS/Data-Modeling-with-Apache-Cassandra/blob/main/images/event_data_image.png" width="80%">
</div>

- `Apache_Cassandra_Sparkify.ipynb`:
  - ETL pipeline for compiling the day-by-day event files into a single csv with the desired columns
  - Data modeling with three queries using [CQL](https://cassandra.apache.org/doc/latest/cassandra/cql/) and creates 3 tables to fit those queries.

<div align="center">
  <img src="https://github.com/Ting-DS/Data-Modeling-with-Apache-Cassandra/blob/main/images/image_event_datafile_new.jpg" width="100%">
</div>

## Libraries 

- **cassandra**
- **cassandra.cluster**
- **os**
- **re**
- **json**
- **csv**


