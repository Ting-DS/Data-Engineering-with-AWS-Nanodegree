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

# Script generated for node step trainer landing
steptrainerlanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="steptrainerlanding_node1",
)

# Script generated for node customer curated
customercurated_node1695411741180 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house/customer/curated"],
        "recurse": True,
    },
    transformation_ctx="customercurated_node1695411741180",
)

# Script generated for node Renamed keys for Step trainer Filter
RenamedkeysforSteptrainerFilter_node1695428446736 = ApplyMapping.apply(
    frame=steptrainerlanding_node1,
    mappings=[
        ("sensorReadingTime", "long", "sensorReadingTime", "long"),
        ("serialNumber", "string", "right_serialNumber", "string"),
        ("distanceFromObject", "int", "distanceFromObject", "int"),
    ],
    transformation_ctx="RenamedkeysforSteptrainerFilter_node1695428446736",
)

# Script generated for node Step trainer Filter
SteptrainerFilter_node1695412248377 = Join.apply(
    frame1=customercurated_node1695411741180,
    frame2=RenamedkeysforSteptrainerFilter_node1695428446736,
    keys1=["serialNumber"],
    keys2=["right_serialNumber"],
    transformation_ctx="SteptrainerFilter_node1695412248377",
)

# Script generated for node Drop PII Fields
DropPIIFields_node1695413545937 = DropFields.apply(
    frame=SteptrainerFilter_node1695412248377,
    paths=["email", "phone", "right_serialNumber"],
    transformation_ctx="DropPIIFields_node1695413545937",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1695427931190 = DynamicFrame.fromDF(
    DropPIIFields_node1695413545937.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicates_node1695427931190",
)

# Script generated for node Step trainer trusted
Steptrainertrusted_node2 = glueContext.write_dynamic_frame.from_options(
    frame=DropDuplicates_node1695427931190,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lake-house/step_trainer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="Steptrainertrusted_node2",
)

job.commit()
