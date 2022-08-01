import os
import glob
import datetime
import random

from dagster import AssetMaterialization, Tuple, asset, multi_asset, Output, Out, build_op_context, job, load_assets_from_current_module, materialize, op, repository, with_resources, MetadataValue
from dagster_aws.s3 import s3_resource
from dagster.utils import file_relative_path

from pandas import DataFrame
import pandas as pd
from pyspark.sql import DataFrame as SparkDF

from modern_data_stack_assets.constants import S3_FAKE_DATA_CONFIG,LOCAL_FAKE_DATA_PATH
from modern_data_stack_assets.partitions import hourly_partitions

from modern_data_stack_assets.fake_source_system.fake_data_generator import generate_fake_data, fake_data_generation_employees, fake_data_generation_content, fake_data_generation_subscription_events, fake_data_generation_subscription_deactivate_events, fake_data_web_events

EMPLOYEES = random.randint(2,4)
ACTIVATIONS = random.randint(45,175)
DEACTIVATIONS = random.randint(5,20)
CONTENT = 30

BACKFILL_DAYS = 2 # number of days to backfill_DAYS

@asset(io_manager_key="parquet_io_manager",compute_kind="python", partitions_def=hourly_partitions,)
def fake_data_employees(context) -> DataFrame:
    context.log.info(f"Downloading fake data")
    current_execution_timestamp = datetime.datetime.now()
    fake_data_employees_generation = fake_data_generation_employees(current_execution_timestamp, EMPLOYEES)
    fake_data_employees_df = DataFrame(fake_data_employees_generation)

    return fake_data_employees_df

@asset(io_manager_key="parquet_io_manager",compute_kind="python", partitions_def=hourly_partitions,)
def fake_content(context, fake_data_employees: SparkDF) -> DataFrame:
    context.log.info(f"Downloading fake data")
    current_execution_timestamp = datetime.datetime.now()
    fake_data_employees = fake_data_employees.toPandas()
    fake_data_employees = fake_data_employees.to_dict('records')
    fake_content_generation = fake_data_generation_content(current_execution_timestamp, CONTENT, fake_data_employees)
    fake_content_df = DataFrame(fake_content_generation)

    return fake_content_df

@asset(io_manager_key="parquet_io_manager",compute_kind="python", partitions_def=hourly_partitions,)
def fake_sub_activate(context) -> DataFrame:
    context.log.info(f"Downloading fake data")
    current_execution_timestamp = datetime.datetime.now()
    fake_sub_activate_generation = fake_data_generation_subscription_events(current_execution_timestamp, ACTIVATIONS)
    fake_sub_activate_df = DataFrame(fake_sub_activate_generation)

    return fake_sub_activate_df

@asset(io_manager_key="parquet_io_manager",compute_kind="python", partitions_def=hourly_partitions,)
def fake_sub_deactivate(context, fake_sub_activate: SparkDF ) -> DataFrame:
    context.log.info(f"Downloading fake data")
    current_execution_timestamp = datetime.datetime.now()
    fake_sub_activate = fake_sub_activate.toPandas()
    fake_sub_activate = fake_sub_activate.to_dict('records')[0:DEACTIVATIONS]
    fake_sub_deactivate_generation = fake_data_generation_subscription_deactivate_events(current_execution_timestamp, fake_sub_activate)
    fake_sub_deactivate_df = DataFrame(fake_sub_deactivate_generation)

    return fake_sub_deactivate_df

@asset(io_manager_key="parquet_io_manager",compute_kind="python", partitions_def=hourly_partitions,)
def fake_web_events(context, fake_sub_activate: SparkDF, fake_content: SparkDF) -> DataFrame:
    context.log.info(f"Downloading fake data")
    current_execution_timestamp = datetime.datetime.now()
    fake_sub_activate = fake_sub_activate.toPandas()
    fake_content = fake_content.toPandas()
    fake_sub_activate = fake_sub_activate.to_dict('records')
    fake_content = fake_content.to_dict('records')
    fake_web_events_generation = fake_data_web_events(current_execution_timestamp, fake_sub_activate, fake_content)
    fake_web_events_df = DataFrame(fake_web_events_generation)

    return fake_web_events_df


@asset(
    io_manager_key="warehouse_io_manager",
    compute_kind="pyspark",
    partitions_def=hourly_partitions,
    key_prefix=["snowflake", "website"],
)
def content(fake_content: SparkDF) -> SparkDF:
    return fake_content

@asset(
    io_manager_key="warehouse_io_manager",
    compute_kind="pyspark",
    partitions_def=hourly_partitions,
    key_prefix=["snowflake", "website"],
)
def sub_activate(fake_sub_activate: SparkDF) -> SparkDF:
    return fake_sub_activate

@asset(
    io_manager_key="warehouse_io_manager",
    compute_kind="pyspark",
    partitions_def=hourly_partitions,
    key_prefix=["snowflake", "website"],
)
def sub_deactivate(fake_sub_deactivate: SparkDF) -> SparkDF:
    return fake_sub_deactivate

@asset(
    io_manager_key="warehouse_io_manager",
    compute_kind="pyspark",
    partitions_def=hourly_partitions,
    key_prefix=["snowflake", "website"],
)
def web_events(fake_web_events: SparkDF) -> SparkDF:
    return fake_web_events

@asset(
    io_manager_key="warehouse_io_manager",
    compute_kind="pyspark",
    partitions_def=hourly_partitions,
    key_prefix=["snowflake", "workday"],
)
def data_employees(fake_data_employees: SparkDF) -> SparkDF:
    return fake_data_employees
