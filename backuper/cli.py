# -*- coding: utf-8 -*-

"""Console script for backuper."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for backuper."""
    click.echo("Replace this message by putting your code into "
               "backuper.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
