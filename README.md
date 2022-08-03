# TODO
- dbt metrics layer
- re data for monitoring / 
- maybe just run great expectations at end
- soda at end
- slim CICD for dbt layer
- sometimes getting failures due to locks on duckdb - look for retry logic
- airbyte dagster have removed for now - will add in for other API data
- great expectations on assets - waiting for dagster blog post

## Nice to do
- duckdb need to create schema every time i delete the db. How to allow creating schema at same time?
- currently using s3 client has no type hints. Could use https://pypi.org/project/boto3-stubs/
- simplify airbyte dependencies
- make the fake data generator `path_to_fake_data` dynamic

## simplify airbyte dependencies

the dagit airbyte software defined asset function doesnt support adding input dependencies via the function `build_airbyte_assets()`

The work around is to generate the `AssetDefintion` for airbyte manually and pass input `AssetDefinition`. I couldnt alter `build_airbyte_assets()` to take an input `AssetDefinition` because the asset creation via `@Asset` decorator uses the params names e.g. *args instead of the original name of the `AssetDefinition`.

# To show off
## Dagster
- `local development speed`: pipenv install -e and update code that is imediatly available to execute in UI
- pipeline and business logic de coupling, you can `swap resources and IOManagers`
- Restart from a particular point
- `Asset aware` its not just pipelines. Dagster also knows what its pipelines are generating.
- Metadata e.g. tests results

# Fake data

Generates a bunch of csv files in `fake-data-generation/fake-data/` related to our music subscription example project.

```bash
cd fake-data-generation
pipenv install
python generate_fake_data.py
```


# data lake

create a bucket in your s3 account and load data after generating `fake data` in the above step.

```bash
export bucket=dbt-template-project-data; # change this to your own bucket
aws s3 mb s3://${bucket} --region ap-southeast-2;
aws s3 cp fake-data-generation/fake-data/ s3://${bucket} --recursive;
```

clean up
```bash
aws s3 rm s3://${bucket} --recursive
```

# Data Warehouse

```bash
docker-compose -f docker-compose.postgres-wh.yml up
```

docker start dbt-template-project_postgres_1


# Airbyte

Spin up an airflow instance.
```bash
docker-compose -f docker-compose.airbyte.yml up
```

or get airbytes latest docker setup at:

```bash
git clone https://github.com/airbytehq/airbyte.git
cd airbyte
docker-compose up
```

Setup one source for each table:

- fake_content
- fake_data_employees
- fake_sub_activate
- fake_sub_deactivate
- fake_web_events

pattern of files to replicate
*fake_content*.csv
*fake_data_employees*.csv
*fake_sub_activate*.csv
*fake_sub_deactivate*.csv
*fake_web_events*.csv

# Data Orchistration

See data-orchistration/README.md