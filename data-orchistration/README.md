# Intro

This is an example of how to use the Software-Defined Asset APIs alongside Modern Data Stack tools
(specifically, Airbyte and dbt).

[blog](https://dagster.io/blog/software-defined-assets)
[youtube](https://www.youtube.com/watch?v=eS--8brw5YM)
[modern_data_stack_assets airbyte example](https://github.com/dagster-io/dagster/tree/master/examples/modern_data_stack_assets)

# Setup

## Python

To install this example and its python dependencies, run:

```
$ pip install -e .
```

Once you've done this, you can run:

run the daemon if required
```
export DAGSTER_HOME="/home/dave/data-engineering/dbt-template-project/data-orchistration/dagster-local-file-store";
dagster-daemon run;

```

Run the UI
```
export DAGSTER_HOME="/home/dave/data-engineering/dbt-template-project/data-orchistration/dagster-local-file-store";
dagit --port 8002;
```

To view this example in Dagster's UI, Dagit.

If you try to kick off a run immediately, it will fail, as there is no source data to ingest/transform, nor is there an active Airbyte connection. To get everything set up properly, read on.

