import pandas as pd
from timewreport.parser import TimeWarriorParser, TimeWarriorInterval
from typing import TextIO

seconds_per_hour = 3600

def get_intervals(input_stream: TextIO) -> list[TimeWarriorInterval]:
    """Get Timewarrior intervals from input stream."""
    return TimeWarriorParser._TimeWarriorParser__parse_intervals_section(input_stream)

def get_data(intervals: list[TimeWarriorInterval], hours_per_day: float) -> dict:
    """Get data from the Timewarrior intervals."""    
    data = dict(
        Date=[],
        Tags=[],
        Hours=[],
        Days=[]
    )
    
    for interval in intervals:
        data["Date"].append(interval.get_start_date())
        data["Tags"].append(", ".join(interval.get_tags())) 
        duration = interval.get_duration()
        data["Hours"].append(duration.seconds / seconds_per_hour)
        data["Days"].append(duration.seconds / seconds_per_hour / hours_per_day) 
    
    return data

def create_dataframe(data: dict) -> pd.DataFrame:
    """Create a pandas DataFrame from the data."""
    df = pd.DataFrame(data)
    df["Week"] = df.Date.apply(lambda x: x.strftime("W%W"))
    df["Weekday"] = df.Date.apply(lambda x: x.strftime("%a"))
    df = df.set_index(["Week", "Date", "Weekday"], drop=True)
    return df

def get_dataframe(input_stream: TextIO, hours_per_day: float) -> pd.DataFrame:
    """Get a pandas DataFrame from the system standard input."""
    intervals = get_intervals(input_stream)
    data = get_data(intervals, hours_per_day)
    return create_dataframe(data)
