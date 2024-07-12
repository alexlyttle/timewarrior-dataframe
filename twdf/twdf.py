import sys
import argparse

from .dataframe import get_dataframe
from .groupby import aggregate_funcs
from .formatter import format_dataframe

HOURS_PER_DAY_DEFAULT = 7.5
HOURS_FORMAT_DEFAULT = ".2f"
DAYS_FORMAT_DEFAULT = ".3f"

FORMAT_CHOICES = ["table", "csv"]
FORMAT_DEFAULT = "table"

COLUMNS_CHOICES = ["tags", "hours", "days"]
COLUMNS_DEFAULT = ["tags", "hours", "days"]

BY_CHOICES = ["tags", "date", "week", "weekday"]

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
    return get_dataframe(args.input, args.hours_per_day, explode_tags=args.explode_tags)

def default_func(args: argparse.Namespace):
    """Return the dataframe from the input file."""
    # columns = args.columns
    return dataframe(args)

def groupby_func(args: argparse.Namespace):
    """Return the grouped dataframe from the input file."""
    df = dataframe(args)
    by = args.by.capitalize()
    # columns = [column for column in args.columns if column != by]
    return df.groupby(by, sort=False).agg(aggregate_funcs(by))

def get_parent_parser() -> argparse.ArgumentParser:
    """Setup parent parser for common arguments."""
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--format",
        "-f",
        help=f"dataframe output format (default is '{FORMAT_DEFAULT}')",
        default=FORMAT_DEFAULT,
        choices=FORMAT_CHOICES
    )
    parent_parser.add_argument(
        "-i",
        "--input",
        help="input file (default is system standard input)",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parent_parser.add_argument(
        "-c", "--columns",
        help=f"columns to show (default is '{COLUMNS_DEFAULT}')",
        nargs="*",
        type=str,
        default=COLUMNS_DEFAULT,
        choices=COLUMNS_CHOICES,
    )
    parent_parser.add_argument(
        "-e", "--explode-tags",
        help=f"create a separate row for each tag (default is False)",
        action="store_true",
    )
    parent_parser.add_argument(
        "--hours-per-day",
        help=f"hours per day (default is {HOURS_PER_DAY_DEFAULT})",
        type=float,
        default=HOURS_PER_DAY_DEFAULT,
    )
    parent_parser.add_argument(
        "--hours-format",
        help=f"string format to display hours (default is '{HOURS_FORMAT_DEFAULT}')",
        type=str,
        default=HOURS_FORMAT_DEFAULT,
    )
    parent_parser.add_argument(
        "--days-format",
        help=f"string format to display days (default is '{DAYS_FORMAT_DEFAULT}')",
        type=str,
        default=DAYS_FORMAT_DEFAULT,
    )
    return parent_parser
    
def get_parser() -> tuple:
    """Return the parser for the command line interface."""

    parent_parser = get_parent_parser()

    # setup main parser, inheriting from parent parser
    parser = argparse.ArgumentParser(
        description='output timewarrior data as a pandas dataframe',
        parents=[parent_parser],
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(func=default_func)

    # setup subparsers
    subparsers = {}
    _subparsers = parser.add_subparsers(help='sub-commands for data aggregation', dest="subcommand")

    # groupby subcommand, inheriting from parent parser
    subcommand = "groupby"
    subparsers[subcommand] = groupby = _subparsers.add_parser(
        subcommand,
        description="group timewarrior data by a column",
        help="group by a column",
        parents=[parent_parser],
        epilog=GROUPBY_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    groupby.set_defaults(func=groupby_func)
    groupby.add_argument("by", help="column to group by", choices=BY_CHOICES)

    return (parser, subparsers)

def main_cli():
    """Run the command line interface."""
    parser, subparsers = get_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.input.isatty():
        if args.subcommand is None:
            parser.print_usage()
        else:
            subparsers[args.subcommand].print_usage()
        print(
            "twdf: error: system stdin must piped or the following argument is required: --input",
            file=sys.stderr
        )
        return None

    # get the dataframe
    df = args.func(args)
    
    # get columns to display
    columns = []
    for column in args.columns:
        if (c := column.capitalize()) in df.columns:
            # e.g. if the groupby column is in the columns list then it becomes and index
            columns.append(c)
        # else quietly do nothing, as args.columns are validated

    print(
        format_dataframe(
            df[columns],
            fmt=args.format,
            hours_format=args.hours_format,
            days_format=args.days_format,
        )
    )
