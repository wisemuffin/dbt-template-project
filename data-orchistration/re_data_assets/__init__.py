import json
import os

from dagster_dbt.asset_defs import load_assets_from_dbt_manifest
from fake_data_assets.resources import RESOURCES_LOCAL, RESOURCES_PROD, RESOURCES_STAGING

from dagster import materialize, repository, with_resources
from dagster.utils import file_relative_path

# from .sensors.slack_on_failure_sensor import make_slack_on_failure_sensor

DBT_PROJECT_DIR = file_relative_path(__file__, "../../data-transformation/fake_data_dbt")
DBT_PROFILES_DIR = DBT_PROJECT_DIR + "/config"

dbt_assets = load_assets_from_dbt_manifest(
    json.load(open(os.path.join(DBT_PROJECT_DIR, "target", "manifest.json"), encoding="utf-8")),
    io_manager_key="warehouse_io_manager",
    # the schemas are already specified in dbt, so we don't need to also specify them in the key
    # prefix here
    key_prefix=["snowflake"],
    source_key_prefix=["snowflake"],
    select='dbt_template_project'
)
fake_data_assets, fake_data_assets_schedule

all_assets = [*fake_data_assets, *dbt_assets] #,*core_assets , *recommender_assets,  *activity_analytics_assets]
all_jobs = [fake_data_assets_schedule] #, core_assets_schedule, activity_analytics_assets_sensor, recommender_assets_sensor]


resource_defs_by_deployment_name = {
    "prod": RESOURCES_PROD,
    "staging": RESOURCES_STAGING,
    "local": RESOURCES_LOCAL,
}


@repository
def repo_fake_data():
    deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")
    resource_defs = resource_defs_by_deployment_name[deployment_name]

    definitions = [with_resources(all_assets, resource_defs), all_jobs]
    # if deployment_name in ["prod", "staging"]:
    #     definitions.append(make_slack_on_failure_sensor(base_url="my_dagit_url"))

    return definitions

if __name__ == "__main__":
    deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")
    resource_defs = resource_defs_by_deployment_name[deployment_name]
    definitions = with_resources(all_assets, resource_defs)
    materialize(definitions)