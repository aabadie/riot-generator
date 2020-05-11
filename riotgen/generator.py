import os
import click

from .application import generate_application
from .example import generate_example
from .board import generate_board
from .pkg import generate_pkg
from .test import generate_test


@click.group()
def cli():
    pass

@cli.command(help='Bootstrap a RIOT application')
@click.option(
    '-d', '--output_dir', type=click.Path(exists=True), default=os.getcwd())
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for application')
def application(output_dir, interactive, config):
    generate_application(output_dir, interactive, config)


@cli.command(help='Bootstrap a RIOT board support')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for board')
def board(interactive, config):
    generate_board(interactive, config)


@cli.command(help='Bootstrap a RIOT example application')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for example application')
def example(interactive, config):
    generate_example(interactive, config)


@cli.command(help='Bootstrap a RIOT external package')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for package')
def pkg(interactive, config):
    generate_pkg(interactive, config)


@cli.command(help='Bootstrap a RIOT test application')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for test application')
def test(interactive, config):
    generate_test(interactive, config)
