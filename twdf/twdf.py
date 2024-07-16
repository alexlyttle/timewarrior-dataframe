import io
import sys
import shutil
import argparse

from .dataframe import get_dataframe
from .groupby import join_tags
from .formatter import format_dataframe

HOURS_PER_DAY_DEFAULT = 7.5
HOURS_FORMAT_DEFAULT = ".2f"
DAYS_FORMAT_DEFAULT = ".3f"

FORMAT_CHOICES = ["table", "csv"]
FORMAT_DEFAULT = "table"

COLUMNS = ["Tags", "Hours", "Days", "Duration", "Start", "End", "Date", "Time", "Week", "Weekday"]

COLUMNS_CHOICES = COLUMNS
COLUMNS_DEFAULT = ["Tags", "Hours", "Days"]

INDEX_CHOICES = COLUMNS
INDEX_DEFAULT = ["Week", "Date", "Time"]

BY_CHOICES = COLUMNS

DEFAULT_AGG = {
    "Hours": "sum",
    "Days": "sum",
    "Duration": "sum",
    "Start": "min",
    "End": "max",
    "Date": ["first", "last"],
    "Week": "first",
    "Weekday": "first",
    "Tags": join_tags,
}

EPILOG = """examples:
  timew export | twdf               # print dataframe for all timewarrior data

  timew export :week | twdf         # print dataframe for this weeks data

  timew export | twdf --format csv  # print dataframe in CSV format

  timew export > report.json        # save data to file, then
  twdf < report.json                # print dataframe using the < operator, or
  twdf --input report.json          # using the --input argument
"""

GROUPBY_EPILOG = """examples:
  timew export | twdf groupby tags   # print dataframe grouped by tags
"""

def dataframe(args: argparse.Namespace):
    """Return the dataframe from the input file."""
    return get_dataframe(args.input, args.hours_per_day, explode_tags=args.explode_tags, index=args.index)

def default_func(args: argparse.Namespace):
    """Return the dataframe from the input file."""
    return dataframe(args)

def groupby_func(args: argparse.Namespace):
    """Return the grouped dataframe from the input file."""
    df = dataframe(args)
    by = [df[key] for key in args.groupby]  # be explicit to ensure no index/column ambiguity
    return df.groupby(by, sort=False).agg(args.agg)

def plot_func(args: argparse.Namespace):
    """Plot the dataframe."""
    raise NotImplementedError("Plotting is not yet implemented.")
    
def get_parser() -> tuple:
    """Return the parser for the command line interface."""

    # setup main parser, inheriting from parent parser
    parser = argparse.ArgumentParser(
        description='output timewarrior data as a pandas dataframe',
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--format",
        help=f"dataframe output format (default is '{FORMAT_DEFAULT}')",
        default=FORMAT_DEFAULT,
        choices=FORMAT_CHOICES
    )
    parser.add_argument(
        "-i",
        "--input",
        help="input file (default is system standard input)",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file (default is system standard output)",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "--groupby",
        nargs="+",
        help="group by a column",
        type=str.capitalize,
        choices=BY_CHOICES,
    )
    parser.add_argument(
        "--columns",
        help=f"columns to show (default is '{COLUMNS_DEFAULT}')",
        nargs="+",
        type=str.capitalize,
        default=COLUMNS_DEFAULT,
        choices=COLUMNS_CHOICES,
    )
    parser.add_argument(
        "--index",
        help=f"columns to use as dataframe indices (default is '{INDEX_DEFAULT}') - this is ineffective when using groupby",
        nargs="+",
        type=str.capitalize,
        default=INDEX_DEFAULT,
        choices=INDEX_CHOICES,
    )
    parser.add_argument(
        "--explode-tags",
        help=f"create a separate row for each tag (default is False)",
        action="store_true",
    )
    parser.add_argument(
        "--hours-per-day",
        help=f"hours per day (default is {HOURS_PER_DAY_DEFAULT})",
        type=float,
        default=HOURS_PER_DAY_DEFAULT,
    )
    parser.add_argument(
        "--hours-format",
        help=f"string format to display hours (default is '{HOURS_FORMAT_DEFAULT}')",
        type=str,
        default=HOURS_FORMAT_DEFAULT,
    )
    parser.add_argument(
        "--days-format",
        help=f"string format to display days (default is '{DAYS_FORMAT_DEFAULT}')",
        type=str,
        default=DAYS_FORMAT_DEFAULT,
    )
    parser.add_argument(
        "--sort",
        help="sort the dataframe index",
        action="store_true",
    )
    parser.set_defaults(sort=False)
    parser.set_defaults(agg=DEFAULT_AGG)
    parser.set_defaults(line_width="auto")

    return parser

def main_cli():
    """Run the command line interface."""
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.input.isatty():
        parser.print_usage()
        print(
            "twdf: error: system stdin must piped or the following argument is required: --input",
            file=sys.stderr
        )
        return None

    # get the dataframe
    if args.groupby:
        # Assume you never want to display groupby columns
        args.columns = list(set(args.columns) - set(args.groupby))
        df = groupby_func(args)
    else:
        df = default_func(args)
    
    if args.sort:
        df = df.sort_index()

    # get columns to display
    # columns = [column for column in args.columns if column in df.columns]
    # else quietly do nothing, as args.columns are validated
    if args.line_width == "auto":
        terminal_size = shutil.get_terminal_size(fallback=(0, 0))
        args.line_width = terminal_size.columns if terminal_size.columns > 0 else None

    with args.output as file:
        file.write(
            format_dataframe(
                df,
                fmt=args.format,
                hours_format=args.hours_format,
                days_format=args.days_format,
                columns=args.columns,
                line_width=args.line_width,
            )
        )
        file.write("\n")  # write new line at end of file
