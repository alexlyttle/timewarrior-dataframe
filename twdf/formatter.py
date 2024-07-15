import pandas as pd
from typing import Optional

def format_dataframe(df: pd.DataFrame, fmt: str, hours_format: str, days_format: str, columns: Optional[list]=None) -> str:
    """Format the DataFrame."""
    formatters = {
        "Hours": f"{{:{hours_format}}}".format,
        "Days": f"{{:{days_format}}}".format,
    }
    if fmt == "csv":
        return df[columns].to_csv()
    elif fmt == "table":
        return df[columns].to_string(formatters=formatters)  #, columns=columns)
    else:
        raise ValueError("Unknown format")
