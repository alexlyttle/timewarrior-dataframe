def join_tags(tags: list[str]) -> str:
    """Join tags into a single string."""
    individual_tags = []
    for t in tags:
        individual_tags += t.split(", ")

    return ", ".join(set(individual_tags))

def aggregate_funcs(by: str) -> dict:
    """Get aggregation functions for groupby column."""
    funcs = {}
    
    if by == "Tags":
        funcs = {
            "Hours": "sum",
            "Days": "sum"
        }
    
    elif by == "Date":
        funcs = {
            "Tags": join_tags,
            "Hours": "sum",
            "Days": "sum"
        }
    
    elif by == "Week":
        funcs = {
            "Tags": join_tags,
            "Hours": "sum",
            "Days": "sum"
        }
    
    elif by == "Weekday":
        funcs = {
            "Tags": join_tags,
            "Hours": "sum",
            "Days": "sum"
        }

    else:
        raise ValueError("Unknown groupby column.")
    
    return funcs
