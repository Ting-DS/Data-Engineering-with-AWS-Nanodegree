import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Customer Trusted
CustomerTrusted_node1695352358325 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house/customer/trusted"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1695352358325",
)

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house/accelerometer/landing"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerLanding_node1",
)

# Script generated for node Customer Privacy Join
CustomerPrivacyJoin_node1695352623886 = Join.apply(
    frame1=CustomerTrusted_node1695352358325,
    frame2=AccelerometerLanding_node1,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="CustomerPrivacyJoin_node1695352623886",
)

# Script generated for node SQL Query
SqlQuery455 = """
select * 
from myDataSource
where timestamp > sharewithresearchasofdate;
"""
SQLQuery_node1695424762058 = sparkSqlQuery(
    glueContext,
    query=SqlQuery455,
    mapping={"myDataSource": CustomerPrivacyJoin_node1695352623886},
    transformation_ctx="SQLQuery_node1695424762058",
)

# Script generated for node Drop Fields
DropFields_node1695352821990 = DropFields.apply(
    frame=SQLQuery_node1695424762058,
    paths=[
        "serialNumber",
        "shareWithPublicAsOfDate",
        "birthDay",
        "registrationDate",
        "shareWithResearchAsOfDate",
        "customerName",
        "email",
        "lastUpdateDate",
        "phone",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropFields_node1695352821990",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1695352977996 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1695352821990,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://stedi-lake-house/accelerometer/trusted/",
        "partitionKeys": [],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AccelerometerTrusted_node1695352977996",
)

job.commit()
