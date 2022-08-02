import numpy as np
from dagster_postgres.utils import get_conn_string

from dagster.utils import file_relative_path

# =========================================================================
# To get this value, got to each of the airbyte conneciton urls
AIRBYTE_CONNECTION_ID_FAKE_CONTENT = "a40a20e1-89e6-46c3-8538-c973ce044f21"
AIRBYTE_CONNECTION_ID_FAKE_DATA_EMPLOYEES = "4e72f55d-da5f-494b-8f26-a63f9a1985d1"
AIRBYTE_CONNECTION_ID_FAKE_SUB_ACTIVE="e2cc579a-d817-4954-b3dc-72977d3f3d3d"
AIRBYTE_CONNECTION_ID_FAKE_SUB_DEACTIVATE="136235bd-1560-4620-97c8-96103156c1a6"
AIRBYTE_CONNECTION_ID_FAKE_WEB_EVENTS="32e8fa70-a3e4-417b-a91e-2da784964266"
# =========================================================================


def model_func(x, a, b):
    return a * np.exp(b * (x / 10**18 - 1.6095))


PG_SOURCE_CONFIG = {
    "username": "postgres",
    "password": "password123",
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
}
PG_DESTINATION_CONFIG = {
    "username": "postgres",
    "password": "password123",
    "host": "localhost",
    "port": 5432,
    "database": "postgres_replica",
}

AIRBYTE_CONFIG = {"host": "localhost", "port": "8000"}
DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt")
DBT_PROFILES_DIR =  file_relative_path(__file__, "../../dbt/config")
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR, "ignore_handled_error": False}
PANDAS_IO_CONFIG = {
    "con_string": get_conn_string(
        username=PG_DESTINATION_CONFIG["username"],
        password=PG_DESTINATION_CONFIG["password"],
        hostname=PG_DESTINATION_CONFIG["host"],
        port=str(PG_DESTINATION_CONFIG["port"]),
        db_name=PG_DESTINATION_CONFIG["database"],
    )
}
S3_FAKE_DATA_CONFIG = {
                    'region_name': 'ap-southeast-2',
                    'profile_name': 'default'
                }
LOCAL_FAKE_DATA_PATH = file_relative_path(__file__, "../../fake-data-generation/fake-data/")

