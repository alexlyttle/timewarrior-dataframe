def join_tags(tags: list[str], delimiter: str=", ") -> str:
    """Join tags into a single string."""
    individual_tags = []
    for t in tags:
        individual_tags += t.split(delimiter)

    return delimiter.join(set(individual_tags))

def aggregate_funcs(by: str) -> dict:
    """Get aggregation functions for groupby column."""
    funcs = {
        "Hours": "sum",
        "Days": "sum"
    }    

    if by in {"Date", "Week", "Weekday"}:
        funcs["Tags"] = join_tags,
    elif by != "Tags":
        raise ValueError("Unknown groupby column.")

    return funcs
