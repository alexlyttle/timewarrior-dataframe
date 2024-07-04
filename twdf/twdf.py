import sys
import argparse

from .dataframe import get_dataframe
from .groupby import aggregate_funcs
from .formatter import format_dataframe

FORMAT_CHOICES = ["table", "csv"]
FORMAT_DEFAULT = "table"

BY_CHOICES = ["tags", "date", "week"]

EPILOG = """examples:
  timew export | twdf               # print dataframe for all timewarrior data

  timew export :week | twdf         # print dataframe for this weeks data

  timew export | twdf --format csv  # print dataframe in CSV format

  timew export > report.json        # save data to file, then
  twdf < report.json                # print dataframe using the < operator, or
  twdf --input report.json          # using the --input argument
"""

GROUBY_EPILOG = """examples:
  timew export | twdf grouby tags   # print dataframe grouped by tags
"""

def default_func(args):
    """Return the dataframe from the input file."""
    return get_dataframe(args.input)

def groupby_func(args):
    """Return the grouped dataframe from the input file."""
    df = get_dataframe(args.input)
    by = args.by.capitalize()
    return df.groupby(by).agg(aggregate_funcs(by))

def get_parser() -> argparse.ArgumentParser:
    """Return the parser for the command line interface."""

    # setup parent parser for common arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--format",
        "-f", 
        help=f"dataframe output format (default is '{FORMAT_DEFAULT}')",
        default=FORMAT_DEFAULT,
        choices=FORMAT_CHOICES
    )
    parent_parser.add_argument(
        "--input",
        help="input file (default is system standard input)",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    
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
        epilog=GROUBY_EPILOG,
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
    
    df = args.func(args)
    print(format_dataframe(df, fmt=args.format))
