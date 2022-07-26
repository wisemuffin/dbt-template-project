import os
import glob

from dagster import AssetMaterialization, asset, build_op_context, job, load_assets_from_current_module, materialize, op, repository, with_resources, MetadataValue
from dagster_aws.s3 import s3_resource
from dagster.utils import file_relative_path

from modern_data_stack_assets.constants import S3_FAKE_DATA_CONFIG,LOCAL_FAKE_DATA_PATH

from fake_data_generator import generate_fake_data

@asset(compute_kind="python")
def fake_data_generation():
    """Model parameters that best fit the observed data"""
    generate_fake_data()


"""
This example show how to turn the s3 session for an op into an asset materialization

If you were to do this via the CLI:
export bucket=dbt-template-project-data; # change this to your own bucket
aws s3 mb s3://${bucket} --region ap-southeast-2;
aws s3 cp fake-data-generation/fake-data/ s3://${bucket} --recursive;
"""

def get_website_data(context, bucket, path, file_partition):
    files=[]
    for file in glob.glob(path + f'{file_partition}*.csv'):
        print(file)
        files.append(file)

    s3_client = context.resources.s3
    for file in files:
        res = s3_client.upload_file(file, bucket, os.path.basename(file))

        print(f'logging content of bucket {bucket} as:  {res}')
    
    context.log_event(
        AssetMaterialization(
            asset_key="my_dataset", description="Persisted result to storage",
            metadata={
                "text_metadata": "Text-based metadata for this event",
                "path": MetadataValue.path(bucket),
                "dashboard_url": MetadataValue.url(
                    "http://wisemuffin.com"
                )
            },
        )
    )

@asset(required_resource_keys={'s3'}, compute_kind="aws cli")
def fake_website(context,fake_data_generation):
    """contains movie content, and web events"""

    bucket = 'dbt-template-project-data'
    path = LOCAL_FAKE_DATA_PATH

    get_website_data(context, bucket, path, file_partition = 'fake_content')
    get_website_data(context, bucket, path, file_partition = 'fake_sub_activate')
    get_website_data(context, bucket, path, file_partition = 'fake_sub_deactivate')
    get_website_data(context, bucket, path, file_partition = 'fake_web_events')
    

@asset(required_resource_keys={'s3'}, compute_kind="aws cli")
def fake_workday(context, fake_data_generation):
    """contains HR data"""

    bucket = 'dbt-template-project-data'
    path = LOCAL_FAKE_DATA_PATH
    file_partition = 'fake_data_employees'
    files=[]
    for file in glob.glob(path + f'{file_partition}*.csv'):
        print(file)
        files.append(file)

    s3_client = context.resources.s3
    for file in files:
        res = s3_client.upload_file(file, bucket, os.path.basename(file))

        print(f'logging content of bucket {bucket} as:  {res}')
    
    context.log_event(
        AssetMaterialization(
            asset_key="my_dataset", description="Persisted result to storage",
            metadata={
                "text_metadata": "Text-based metadata for this event",
                "path": MetadataValue.path(bucket),
                "dashboard_url": MetadataValue.url(
                    "http://wisemuffin.com"
                )
            },
        )
    )

resource_defs = {
    "s3": s3_resource.configured(S3_FAKE_DATA_CONFIG)
}


if __name__ == "__main__":
    assets_to_load = with_resources(
        load_assets_from_current_module(),
        resource_defs=resource_defs,
    )
    materialize(assets_to_load)