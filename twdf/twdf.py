import sys
import argparse

from .dataframe import get_dataframe
from .groupby import aggregate_funcs
from .formatter import format_dataframe

FORMAT_CHOICES = ["table", "csv"]
FORMAT_DEFAULT = "table"
BY_CHOICES = ["tags", "date", "week"]

def default_func(args):
    return get_dataframe(args.input)

def groupby_func(args):
    df = get_dataframe(args.input)
    by = args.by.capitalize()
    return df.groupby(by).agg(aggregate_funcs(by))

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='output timewarrior data as a pandas dataframe')
    parser.add_argument(
        "--input",
        help="input file (default is system standard input)",
        type=argparse.FileType("r"),
        default=sys.stdin
    )
    parser.add_argument("--format", "-f", help=f"dataframe output format (default is '{FORMAT_DEFAULT}')", default=FORMAT_DEFAULT, choices=FORMAT_CHOICES)
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='sub-commands for data aggregation')

    groupby = subparsers.add_parser('groupby', help='Group by a column')
    groupby.add_argument("by", help="column to group by", choices=BY_CHOICES)
    groupby.set_defaults(func=groupby_func)
    
    return parser

def main_cli():
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    df = args.func(args)
    print(format_dataframe(df, fmt=args.format))
