import logging
import click

from .application import application
from .board import board
from .test import test

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)14s - '
                           '%(levelname)5s - %(message)s')
logger = logging.getLogger("riotgen.generator")


@click.group()
def cli():
    pass

# register subcommands
cli.add_command(application)
cli.add_command(board)
cli.add_command(test)