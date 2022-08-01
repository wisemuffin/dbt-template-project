from modern_data_stack_assets.partitions import hourly_partitions

from dagster import (
    AssetSelection,
    build_schedule_from_partitioned_job,
    define_asset_job,
    load_assets_from_package_module,
)

from . import assets

FAKE_DATA = "fake_data"

fake_data_assets = load_assets_from_package_module(package_module=assets, group_name=FAKE_DATA)

RUN_TAGS = {
    "dagster-k8s/config": {
        "container_config": {
            "resources": {
                "requests": {"cpu": "500m", "memory": "2Gi"},
            }
        },
    }
}

fake_data_assets_schedule = build_schedule_from_partitioned_job(
    define_asset_job(
        "fake_data_job",
        selection=AssetSelection.groups(FAKE_DATA),
        tags=RUN_TAGS,
        partitions_def=hourly_partitions,
    )
)
