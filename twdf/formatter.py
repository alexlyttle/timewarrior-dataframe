import pandas as pd
from typing import Optional

def format_dataframe(df: pd.DataFrame, fmt: str, hours_format: str, days_format: str, columns: Optional[list]=None,
                     line_width: int=None) -> str:
    """Format the DataFrame."""
    # TODO: replace with a more general solution which takes a dictionary of columns and formats
    # should account for choice of aggregation functions
    formatters = {
        "Hours": f"{{:{hours_format}}}".format,
        "Days": f"{{:{days_format}}}".format,
        ("Hours", "sum"): f"{{:{hours_format}}}".format,
        ("Days", "sum"): f"{{:{days_format}}}".format,
    }
    if fmt == "csv":
        return df[columns].to_csv()
    elif fmt == "table":
        return df[columns].to_string(formatters=formatters, line_width=line_width)  #, columns=columns)
    else:
        raise ValueError("Unknown format")
