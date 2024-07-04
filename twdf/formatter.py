import pandas as pd


def format_dataframe(df: pd.DataFrame, fmt: str, hours_format: str, days_format: str) -> str:
    """Format the DataFrame."""
    formatters = {
        "Hours": f"{{:{hours_format}}}".format,
        "Days": f"{{:{days_format}}}".format,
    }
    if fmt == "csv":
        return df.to_csv()
    elif fmt == "table":
        return df.to_string(formatters=formatters)
    else:
        raise ValueError("Unknown format")
