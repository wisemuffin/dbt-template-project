```shell
datahub docker quickstart
```
# upgrading 
simply issue command again
```bash
datahub docker quickstart
```

# local website

http://localhost:9002/

# reset data

```bash
datahub docker nuke
```

# backup

```bash
datahub docker quickstart --backup
datahub docker quickstart --restore
```

# Data ingestion

dbt compile --exclude re_data

```bash
dbt run --exclude package:re_data
dbt docs generate --no-compile

datahub ingest -c fake_data_dbt_to_datahub.dhub.yaml
```