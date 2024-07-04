import pandas as pd

formatters = {
    "Hours": "{:.2f}".format,
    "Days": "{:.3f}".format,
}

def format_dataframe(df: pd.DataFrame, fmt) -> str:
    """Format the DataFrame."""
    if fmt == "csv":
        return df.to_csv()
    elif fmt == "table":
        return df.to_string(formatters=formatters)
    else:
        raise ValueError("Unknown format")
