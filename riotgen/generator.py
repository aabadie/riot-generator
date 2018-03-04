import logging
import click

from riotgen.application import generate_application
from riotgen.example import generate_example
from riotgen.board import generate_board
from riotgen.pkg import generate_pkg
from riotgen.test import generate_test

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)14s - '
                           '%(levelname)5s - %(message)s')
logger = logging.getLogger("riotgen.generator")


@click.group()
def cli():
    pass


@cli.command(help='Bootstrap a RIOT application')
@click.argument('output_dir', type=click.Path(exists=True))
@click.option('--config', type=click.File(mode='r'),
              help='Application initial configuration file')
def application(output_dir, config):
    generate_application(output_dir, config)


@cli.command(help='Bootstrap a RIOT board support')
@click.option('--config', type=click.File(mode='r'),
              help='Board support initial configuration file')
def board(config):
    generate_board(config)


@cli.command(help='Bootstrap a RIOT example application')
@click.option('--config', type=click.File(mode='r'),
              help='Example application initial configuration file')
def example(config):
    generate_example(config)


@cli.command(help='Bootstrap a RIOT external package')
@click.option('--config', type=click.File(mode='r'),
              help='Package initial configuration file')
def pkg(config):
    generate_pkg(config)


@cli.command(help='Bootstrap a RIOT test application')
@click.option('--config', type=click.File(mode='r'),
              help='Test application initial configuration file')
def test(config):
    generate_test(config)


if __name__ == '__main__':
    cli()