# timewarrior-dataframe

Timewarrior command-line interface (CLI) for producing pandas dataframes.

## Install

```bash
pip install git+https://github.com/alexlyttle/timewarrior-dataframe.git
```

## Usage

Pipe the output of `timew export` to the `twdf` script,

```bash
timew export | twdf
```

outputs a pandas DataFrame as a string.

You can use the usual options and hints with `timew export`, e.g.

```bash
timew export :week | twdf
```

will only output data for the current week.

### Format

Choose between table (default) or CSV format with the `--format` option, e.g.

```bash
timew export | twdf --format csv
```

### Input

By default, the `twdf` command expects input JSON data from the system standard input (e.g. using the `|` operator).
If the output of `timew export` has been saved to a file elsewhere, then you can redirect the file contents with `<` operator or by using the `--input` option.

For example, if you have saved Timewarrior data with the following command,

```bash
timew export > report.json
```

you can direct the contents of this file to `twdf` with either of the following commands,

```bash
twdf < report.json
twdf --input report.json
```

### Groupby

Group the table by tags, date, or week with the `groupby` subcommand, e.g.

```bash
timew export | twdf groupby tags
```
