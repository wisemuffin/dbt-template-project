from typing import List, Mapping, Optional, Set

from dagster_airbyte.utils import generate_materializations

from dagster import AssetIn, AssetKey, Out, Output
from dagster import _check as check
from dagster.core.definitions import AssetsDefinition, multi_asset
from dagster.utils.backcompat import experimental

from modern_data_stack_assets_old.fake_source_system.assets.fake_source_systems import fake_website, fake_workday


"""
Note issue - i cant use build_airbyte_assets to add input dependenci🇪🇪 
As a workaround i have added the fake source systems as asset dependcies within the 
`build_airbyte_assets_dg()`
 
"""

@experimental
def build_airbyte_assets_dg(
    connection_id: str,
    destination_tables: List[str],
    asset_key_prefix: Optional[List[str]] = None,
    **kwargs,
) -> List[AssetsDefinition]:
    """
    Builds a set of assets representing the tables created by an Airbyte sync operation.

    Args:
        connection_id (str): The Airbyte Connection ID that this op will sync. You can retrieve this
            value from the "Connections" tab of a given connector in the Airbyte UI.
        destination_tables (List[str]): The names of the tables that you want to be represented
            in the Dagster asset graph for this sync. This will generally map to the name of the
            stream in Airbyte, unless a stream prefix has been specified in Airbyte.
        asset_key_prefix (Optional[List[str]]): A prefix for the asset keys inside this asset.
            If left blank, assets will have a key of `AssetKey([table_name])`.
    """

    asset_key_prefix = check.opt_list_param(asset_key_prefix, "asset_key_prefix", of_type=str)

    @multi_asset(
        name=f"airbyte_sync_{connection_id[:5]}",
        outs={
            table: Out(
                asset_key=AssetKey(
                    asset_key_prefix + [table],
                )
            )
            for table in destination_tables
        },
        required_resource_keys={"airbyte"},
        compute_kind="airbyte",
    )
    def _assets(context, fake_website, fake_workday):
        ab_output = context.resources.airbyte.sync_and_poll(connection_id=connection_id)
        for materialization in generate_materializations(ab_output, asset_key_prefix):
            table_name = materialization.asset_key.path[-1]
            if table_name in destination_tables:
                yield Output(
                    value=None,
                    output_name=table_name,
                    metadata={
                        entry.label: entry.entry_data for entry in materialization.metadata_entries
                    },
                )
            else:
                yield materialization

    return [_assets]
