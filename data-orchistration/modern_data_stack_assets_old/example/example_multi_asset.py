from dagster import AssetKey, Out, Output, asset, multi_asset


@asset
def a():
    print('a')

@asset
def b():
    print('a')

@multi_asset(
    outs={"c": Out(), "d": Out()},
    internal_asset_deps={
        "c": {AssetKey("a")},
        "d": {AssetKey("b")},
    },
)
def my_complex_assets(context, a, b):
    # c only depends on a
    yield Output(value=a + 1, output_name="c")
    # d only depends on b
    yield Output(value=b + 1, output_name="d")
