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


class SharedCommand(click.core.Command):
    """Class for shared subcommand options"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = [
            click.core.Option(
                (
                    "-i",
                    "--interactive",
                ),
                is_flag=True,
                help="Use interactive mode",
            ),
            click.core.Option(
                (
                    "-c",
                    "--config",
                ),
                type=click.File(mode="r"),
                help="Use a configuration file",
            ),
            click.core.Option(
                ("-r", "--riotbase"),
                type=click.Path(exists=True),
                default=os.getenv("RIOTBASE"),
            ),
        ]
        self.params += options


@click.group()
@click.version_option(version=__version__)
def riotgen():  # pylint:disable=missing-function-docstring
    pass


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT application")
@click.option(
    "-d",
    "--output-dir",
    type=click.Path(exists=True),
    default=os.getcwd(),
    show_default="current directory",
)
def application(output_dir, interactive, config, riotbase):
    """Entry point for application subcommand."""
    generate_application(output_dir, interactive, config, riotbase)


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT board support")
def board(interactive, config, riotbase):
    """Entry point for board subcommand."""
    generate_board(interactive, config, riotbase)


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT driver module")
def driver(interactive, config, riotbase):
    """Entry point for driver subcommand."""
    generate_driver(interactive, config, riotbase)


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT example application")
def example(interactive, config, riotbase):
    """Entry point for example application subcommand."""
    generate_example(interactive, config, riotbase)


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT system module")
def module(interactive, config, riotbase):
    """Entry point for module subcommand."""
    generate_module(interactive, config, riotbase)


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT external package")
def pkg(interactive, config, riotbase):
    """Entry point for pkg subcommand."""
    generate_pkg(interactive, config, riotbase)


@riotgen.command(cls=SharedCommand, help="Bootstrap a RIOT test application")
def test(interactive, config, riotbase):
    """Entry point for test subcommand."""
    generate_test(interactive, config, riotbase)
