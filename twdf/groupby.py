import pandas as pd
from typing import Union

def join_tags(tags: list[str], delimiter: str=", ") -> str:
    """Join tags into a single string."""
    individual_tags = []
    for t in tags:
        individual_tags += t.split(delimiter)

    return delimiter.join(set(individual_tags))
