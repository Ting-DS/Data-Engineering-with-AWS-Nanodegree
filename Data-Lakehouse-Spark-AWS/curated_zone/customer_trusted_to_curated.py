import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Customer Trusted
CustomerTrusted_node1695352358325 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi2",
    table_name="customer_trusted",
    transformation_ctx="CustomerTrusted_node1695352358325",
)

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi2",
    table_name="accelerometer_landing",
    transformation_ctx="AccelerometerLanding_node1",
)

# Script generated for node Customer Privacy Join
CustomerPrivacyJoin_node1695352623886 = Join.apply(
    frame1=AccelerometerLanding_node1,
    frame2=CustomerTrusted_node1695352358325,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="CustomerPrivacyJoin_node1695352623886",
)

# Script generated for node Drop Fields
DropFields_node1695352821990 = DropFields.apply(
    frame=CustomerPrivacyJoin_node1695352623886,
    paths=["user", "timestamp", "x", "y", "z"],
    transformation_ctx="DropFields_node1695352821990",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1695426820996 = DynamicFrame.fromDF(
    DropFields_node1695352821990.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicates_node1695426820996",
)

# Script generated for node Customer Curated
CustomerCurated_node1695352977996 = glueContext.write_dynamic_frame.from_options(
    frame=DropDuplicates_node1695426820996,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lake-house/customer/curated/",
        "partitionKeys": [],
    },
    transformation_ctx="CustomerCurated_node1695352977996",
)

job.commit()
