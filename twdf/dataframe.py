import pandas as pd
from timewreport.parser import TimeWarriorParser, TimeWarriorInterval
from typing import TextIO, Optional
from collections import defaultdict

SECONDS_PER_HOUR = 3600

def get_intervals(input_stream: TextIO) -> list[TimeWarriorInterval]:
    """Get Timewarrior intervals from input stream."""
    return TimeWarriorParser._TimeWarriorParser__parse_intervals_section(input_stream)

def get_data(intervals: list[TimeWarriorInterval], hours_per_day: float) -> dict:
    """Get data from the Timewarrior intervals."""    
    data = defaultdict(list)

    for interval in intervals:
        start = interval.get_start()
        
        data["Start"].append(start)
        data["End"].append(interval.get_end())  
        
        data["Date"].append(start.date())
        data["Time"].append(start.time())
        data["Week"].append(int(start.strftime("%W")))
        data["Weekday"].append(start.strftime("%a"))

        data["Tags"].append(", ".join(interval.get_tags()))

        duration = interval.get_duration()
        data["Duration"].append(duration)
        data["Hours"].append(duration.seconds / SECONDS_PER_HOUR)
        data["Days"].append(duration.seconds / SECONDS_PER_HOUR / hours_per_day) 
    
    return data

def explode(df: pd.DataFrame, column: str, delimiter: str=", ") -> pd.DataFrame:
    """Explode a column with comma separated values."""
    exploded_tags = df[column].str.split(delimiter).explode()
    return df.drop(columns=column).join(exploded_tags)

def create_dataframe(data: dict, explode_tags: bool=False, index: Optional[list]=None) -> pd.DataFrame:
    """Create a pandas DataFrame from the data."""
    df = pd.DataFrame(data)
    # df["Week"] = df.Date.apply(lambda x: x.strftime("%W")).astype(int)
    # df["Weekday"] = df.Date.apply(lambda x: x.strftime("%a"))
    if explode_tags:
        df = explode(df, "Tags")
    if index is not None:
        df = df.set_index(index, drop=False)
    return df
    
def get_dataframe(input_stream: TextIO, hours_per_day: float, explode_tags: bool=False, index: Optional[list]=None) -> pd.DataFrame:
    """Get a pandas DataFrame from the system standard input."""
    intervals = get_intervals(input_stream)
    data = get_data(intervals, hours_per_day)
    return create_dataframe(data, explode_tags=explode_tags, index=index)
