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
@click.option(
    '-r', '--riotbase', type=click.Path(exists=True),
    default=os.getenv('RIOTBASE'))
def application(output_dir, interactive, config, riotbase):
    generate_application(output_dir, interactive, config, riotbase)


@cli.command(help='Bootstrap a RIOT board support')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for board')
@click.option(
    '-r', '--riotbase', type=click.Path(exists=True),
    default=os.getenv('RIOTBASE'))
def board(interactive, config, riotbase):
    generate_board(interactive, config, riotbase)


@cli.command(help='Bootstrap a RIOT example application')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for example application')
@click.option(
    '-r', '--riotbase', type=click.Path(exists=True),
    default=os.getenv('RIOTBASE'))
def example(interactive, config, riotbase):
    generate_example(interactive, config, riotbase)


@cli.command(help='Bootstrap a RIOT external package')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for package')
@click.option(
    '-r', '--riotbase', type=click.Path(exists=True),
    default=os.getenv('RIOTBASE'))
def pkg(interactive, config, riotbase):
    generate_pkg(interactive, config, riotbase)


@cli.command(help='Bootstrap a RIOT test application')
@click.option('-i', '--interactive', is_flag=True, help='Use interactive mode')
@click.option('--config', type=click.File(mode='r'),
              help='Configuration file for test application')
@click.option(
    '-r', '--riotbase', type=click.Path(exists=True),
    default=os.getenv('RIOTBASE'))
def test(interactive, config, riotbase):
    generate_test(interactive, config, riotbase)
