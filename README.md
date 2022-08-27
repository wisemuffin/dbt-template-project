# TODO
- datahub 
    - dbt 
        - docs
    - great expecation validation
- dbt metrics layer
- re data for monitoring / 
- maybe just run great expectations at end
- soda at end
- slim CICD for dbt layer
- sometimes getting failures due to locks on duckdb - look for retry logic
- airbyte dagster have removed for now - will add in for other API data
- great expectations on assets - waiting for dagster blog post
- switch s3 to mino

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


# Data Lake

## legacy load into data lake

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

# Data Warehouse [Legeacy]

```bash
cd data-infra
docker-compose -f docker-compose.postgres-wh.yml up
```

docker start dbt-template-project_postgres_1


# Airbyte

Spin up an airbyte instance.
```bash
cd data-infra
docker-compose -f docker-compose.airbyte.yml up
```

or get airbytes latest docker setup at:

```bash
git clone https://github.com/airbytehq/airbyte.git
cd airbyte
docker-compose up
```
# Data transofmation dbt

limiations
- dbt does not support freshness of non sources: https://github.com/dbt-labs/dbt-core/issues/3862

## dbt yaml

[vscode setup for autocomplete](https://github.com/dbt-labs/dbt-jsonschema)

# Data Orchistration

See data-orchistration/README.md

# Data Catalog

## Datahub

Limitations
- dbt source freshness no longer working https://feature-requests.datahubproject.io/p/support-dbt-source-freshness
- re_data is stopping descriptions and tests getting updated.

# Data Monitoring

```bash
cd ./data-transformation/fake_data_dbt;
dbt run --models package:re_data;
```

***cant generate website not supported with duckdb*** Catalog Error: Scalar Function with name date does not exist!
```bash
re_data overview generate --start-date 2022-08-15 --interval days:1;
re_data overview serve;
```

## workaround re_data & duckdb compatibility issues
***this doesnt fix*** the issue when running re_data overview generate

error when using re_data and duckdb when creating re_data_last_stats:

Error: Parser Error: ORDER BY is not implemented for window functions!

work around add:

/home/dave/data-engineering/dbt-template-project/data-transformation/fake_data_dbt/dbt_packages/fivetran_utils/macros/percentile.sql

```sql
{% macro duckdb__percentile(percentile_field, partition_field, percent)  %}

    quantile_cont( 
        {{ percentile_field }}, 
        {{ percent }}) 
        over (partition by {{ partition_field }}    
        )

{% endmacro %}
```

/home/dave/data-engineering/dbt-template-project/data-transformation/fake_data_dbt/dbt_packages/re_data/macros/db/core/split_and_return_nth_value.sql

```sql
{% macro duckdb__split_and_return_nth_value(column_name, delimiter, ordinal) -%}
    str_split({{ re_data.clean_blacklist(column_name, ['"', '`'], '') }}, '{{ delimiter }}', {{ ordinal }})[2]
{%- endmacro %}
```

comment out
in: /home/dave/data-engineering/dbt-template-project/data-transformation/fake_data_dbt/dbt_packages/re_data/models/alerts/re_data_anomalies.sql

```jinja
    'turned off workaround dg' as message,
    'turned off workaround dg' as last_value_text
    {# {{ re_data.generate_anomaly_message('z.column_name', 'z.metric', 'z.last_value', 'z.last_avg') }} as message,
    {{ re_data.generate_metric_value_text('z.metric', 'z.last_value') }} as last_value_text #}
```