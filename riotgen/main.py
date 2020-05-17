"""riotgen main module."""

import os
import click

from .application import generate_application
from .example import generate_example
from .board import generate_board
from .driver import generate_driver
from .module import generate_module
from .pkg import generate_pkg
from .test import generate_test
from . import __version__


@click.group()
@click.version_option(version=__version__)
def riotgen():  # pylint:disable=missing-function-docstring
    pass


@riotgen.command(help="Bootstrap a RIOT application")
@click.option("-d", "--output_dir", type=click.Path(exists=True), default=os.getcwd())
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c",
    "--config",
    type=click.File(mode="r"),
    help="Configuration file for application",
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def application(output_dir, interactive, config, riotbase):
    """Entry point for application subcommand."""
    generate_application(output_dir, interactive, config, riotbase)


@riotgen.command(help="Bootstrap a RIOT board support")
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c", "--config", type=click.File(mode="r"), help="Configuration file for board"
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def board(interactive, config, riotbase):
    """Entry point for board subcommand."""
    generate_board(interactive, config, riotbase)


@riotgen.command(help="Bootstrap a RIOT driver module")
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c",
    "--config",
    type=click.File(mode="r"),
    help="Configuration file for the driver module",
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def driver(interactive, config, riotbase):
    """Entry point for driver subcommand."""
    generate_driver(interactive, config, riotbase)


@riotgen.command(help="Bootstrap a RIOT example application")
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c",
    "--config",
    type=click.File(mode="r"),
    help="Configuration file for example application",
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def example(interactive, config, riotbase):
    """Entry point for example application subcommand."""
    generate_example(interactive, config, riotbase)


@riotgen.command(help="Bootstrap a RIOT system module")
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c",
    "--config",
    type=click.File(mode="r"),
    help="Configuration file for the system module",
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def module(interactive, config, riotbase):
    """Entry point for module subcommand."""
    generate_module(interactive, config, riotbase)


@riotgen.command(help="Bootstrap a RIOT external package")
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c", "--config", type=click.File(mode="r"), help="Configuration file for package"
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def pkg(interactive, config, riotbase):
    """Entry point for pkg subcommand."""
    generate_pkg(interactive, config, riotbase)


@riotgen.command(help="Bootstrap a RIOT test application")
@click.option("-i", "--interactive", is_flag=True, help="Use interactive mode")
@click.option(
    "-c",
    "--config",
    type=click.File(mode="r"),
    help="Configuration file for test application",
)
@click.option(
    "-r", "--riotbase", type=click.Path(exists=True), default=os.getenv("RIOTBASE")
)
def test(interactive, config, riotbase):
    """Entry point for test subcommand."""
    generate_test(interactive, config, riotbase)
