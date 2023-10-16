import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={},
    connection_type="s3",
    format="parquet",
    connection_options={
        "paths": ["s3://stedi-lake-house/accelerometer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="accelerometer_trusted_node1",
)

# Script generated for node Step trainer trusted
Steptrainertrusted_node1695431038383 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house/step_trainer/trusted"],
        "recurse": True,
    },
    transformation_ctx="Steptrainertrusted_node1695431038383",
)

# Script generated for node Change Schema
ChangeSchema_node1695434327905 = ApplyMapping.apply(
    frame=accelerometer_trusted_node1,
    mappings=[
        ("z", "double", "z", "double"),
        ("timeStamp", "long", "timeStamp", "bigint"),
        ("user", "string", "user", "string"),
        ("y", "double", "y", "double"),
        ("x", "double", "x", "double"),
    ],
    transformation_ctx="ChangeSchema_node1695434327905",
)

# Script generated for node Drop Fields
DropFields_node1695434261194 = DropFields.apply(
    frame=Steptrainertrusted_node1695431038383,
    paths=[
        "timeStamp",
        "birthDay",
        "shareWithPublicAsOfDate",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropFields_node1695434261194",
)

# Script generated for node Join
Join_node1695431105847 = Join.apply(
    frame1=DropFields_node1695434261194,
    frame2=ChangeSchema_node1695434327905,
    keys1=["sensorReadingTime"],
    keys2=["timeStamp"],
    transformation_ctx="Join_node1695431105847",
)

# Script generated for node S3 bucket
S3bucket_node2 = glueContext.write_dynamic_frame.from_options(
    frame=Join_node1695431105847,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-lake-house/ml/", "partitionKeys": []},
    transformation_ctx="S3bucket_node2",
)

job.commit()
