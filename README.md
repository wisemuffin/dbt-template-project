# Fake data

Generates a bunch of csv files in `fake-data-generation/fake-data/` related to our music subscription example project.

```bash
cd fake-data-generation
pipenv install
python fake-data-generator.py
```


# data lake

create a bucket in your s3 account and load data after generating `fake data` in the above step.

```bash
export bucket=dbt-template-project-data; # change this to your own bucket
aws s3 mb s3://${bucket} --region ap-southeast-2;
aws s3 cp fake-data-generation/fake-data/ s3://${bucket} --recursive;
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
