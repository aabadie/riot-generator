"""RIOT pkg generator module."""

import os

import click

from .common import render_source, render_file, read_config_file
from .common import check_params, prompt_params, prompt_params_list
from .common import check_riotbase


PKG_PARAMS = {
    "name": {"args": ["Package name"], "kwargs": {}},
    "displayed_name": {
        "args": ["Package displayed name (for doxygen documentation)"],
        "kwargs": {}
    },
    "url": {"args": ["Package source url"], "kwargs": {}},
    "hash": {"args": ["Package version hash"], "kwargs": {}},
    "license": {"args": ["Package license"], "kwargs": {}},
    "description": {"args": ["Package short description"], "kwargs": {}},
}

PKG_PARAMS_LIST = ["modules", "packages", "features"]


def generate_pkg(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(param_type="--interactive and/or --config options")

    check_riotbase(riotbase)

    params = {"pkg": {}}

    if config is not None:
        params = read_config_file(config, "board")

    if interactive:
        prompt_params(params, PKG_PARAMS, "pkg")
        prompt_params_list(params, "pkg", *PKG_PARAMS_LIST)

    check_params(params, PKG_PARAMS.keys() ,"pkg")

    pkg_name = params["pkg"]["name"]

    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    pkgs_dir = os.path.join(riotbase, "pkg")
    pkg_dir = os.path.join(pkgs_dir, pkg_name)

    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join("pkg", pkg_name)
    else:
        output_dir = os.path.expanduser(pkg_dir)

    if os.path.exists(pkg_dir) and not click.prompt(
        "'{name}' pkg directory already exists, "
        "overwrite (y/N)?".format(pkg_name),
        default=False,
        show_default=False,
    ):
        click.echo("Abort")
        return

    render_source(
        params,
        "pkg",
        ["doc.txt", "Makefile", "Makefile.dep", "Makefile.include"],
        output_dir,
    )

    template_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", "pkg"
    )
    makefile_pkg_out = os.path.join(output_dir, "{}.mk".format(pkg_name))
    render_file(params, template_dir, "pkg.mk.j2", makefile_pkg_out)

    click.echo(
        click.style(
            "Package '{name}' generated in {output_dir} with success!".format(
                name=pkg_name, output_dir=output_dir
            ),
            bold=True,
        )
    )
