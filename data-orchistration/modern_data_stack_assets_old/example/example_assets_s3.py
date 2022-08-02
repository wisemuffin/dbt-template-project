import os
import glob

from dagster import AssetMaterialization, asset, build_op_context, job, load_assets_from_current_module, materialize, op, repository, with_resources, MetadataValue
from dagster_aws.s3 import s3_resource
from dagster.utils import file_relative_path

from modern_data_stack_assets_old.constants import S3_FAKE_DATA_CONFIG,LOCAL_FAKE_DATA_PATH

# This example show how to turn the s3 session for an op into an asset materialization
# export bucket=dbt-template-project-data; # change this to your own bucket
# aws s3 mb s3://${bucket} --region ap-southeast-2;
# aws s3 cp fake-data-generation/fake-data/ s3://${bucket} --recursive;

@asset(required_resource_keys={'s3'})
def example_s3_asset(context):
    """example of materialisation in op/asset"""

    bucket = 'dbt-template-project-data'
    path = LOCAL_FAKE_DATA_PATH
    file_partition = 'fake_content'
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

    return None


@op(required_resource_keys={'s3'})
def example_s3_op(context):
    """example of materialisation in op"""
    bucket = 'dbt-template-project-data'
    res = context.resources.s3.list_objects_v2(
        Bucket=bucket,
        Prefix=''
    )
    print(f'logging content of bucket {bucket} as:  {res}')
    
    context.log_event(
        AssetMaterialization(
            asset_key="my_dataset", description="Persisted result to storage"
        )
    )

    return res

@job(resource_defs={'s3': s3_resource})
def example_job():
    example_s3_op()
    
resource_defs = {
    "s3": s3_resource.configured(S3_FAKE_DATA_CONFIG)
}

@repository
def s3_example_repo():
    from dagster import define_asset_job

    return with_resources(
        load_assets_from_current_module(),
        resource_defs=resource_defs,
    ) + [define_asset_job("all")] + [example_job]


if __name__ == "__main__":
    assets_to_load = with_resources(
        load_assets_from_current_module(),
        resource_defs=resource_defs,
    )
    materialize(assets_to_load)