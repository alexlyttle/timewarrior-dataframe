DEFAULT_FUNCS = {
    "Hours": "sum",
    "Days": "sum",
    "Duration": "sum",
    "Start": "min",
    "End": "max"
}

def join_tags(tags: list[str], delimiter: str=", ") -> str:
    """Join tags into a single string."""
    individual_tags = []
    for t in tags:
        individual_tags += t.split(delimiter)

    return delimiter.join(set(individual_tags))

def aggregate_funcs(by: str) -> dict:
    """Get aggregation functions for groupby column."""
    funcs = DEFAULT_FUNCS

    if by != "Tags":
        funcs["Tags"] = join_tags

    return funcs
