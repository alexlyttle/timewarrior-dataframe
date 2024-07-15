import pandas as pd
from typing import Union

def join_tags(tags: list[str], delimiter: str=", ") -> str:
    """Join tags into a single string."""
    individual_tags = []
    for t in tags:
        individual_tags += t.split(delimiter)

    return delimiter.join(set(individual_tags))

DEFAULT_FUNCS = {
    "Hours": "sum",
    "Days": "sum",
    "Duration": "sum",
    "Start": "min",
    "End": "max",
    "Date": "first",
    "Week": "first",
    "Weekday": "first",
    "Tags": join_tags,
}

def aggregate_funcs(df: pd.DataFrame, by: Union[str, list]) -> dict:
    """Get aggregation functions for groupby column."""
    # quietly ignore columns not in the dataframe
    return {key: value for key, value in DEFAULT_FUNCS.items() if key in df.columns and not key in by}
