import logging
import click

from .application import generate_application
from .example import generate_example
from .board import generate_board
from .pkg import generate_pkg
from .test import generate_test

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)14s - '
                           '%(levelname)5s - %(message)s')
logger = logging.getLogger("riotgen.generator")


@click.group()
def cli():
    pass

@cli.command(help='Bootstrap a RIOT application')
@click.argument('output_dir', type=click.Path(exists=True))
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Application initial configuration file')
def application(output_dir, interactive, config):
    generate_application(output_dir, interactive, config)


@cli.command(help='Bootstrap a RIOT board support')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Board support initial configuration file')
def board(interactive, config):
    generate_board(interactive, config)


@cli.command(help='Bootstrap a RIOT example application')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Example application initial configuration file')
def example(interactive, config):
    generate_example(interactive, config)


@cli.command(help='Bootstrap a RIOT external package')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Package initial configuration file')
def pkg(interactive, config):
    generate_pkg(interactive, config)


@cli.command(help='Bootstrap a RIOT test application')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Test application initial configuration file')
def test(interactive, config):
    generate_test(interactive, config)
