"""RIOT pkg generator module."""

import click

from .common import render_source, generate


PKG_PARAMS = {
    "name": {"args": ["Package name"], "kwargs": {}},
    "displayed_name": {
        "args": ["Package displayed name (for doxygen documentation)"],
        "kwargs": {},
    },
    "url": {"args": ["Package source url"], "kwargs": {}},
    "hash": {"args": ["Package version hash"], "kwargs": {}},
    "license": {"args": ["Package license"], "kwargs": {}},
    "description": {"args": ["Package short description"], "kwargs": {}},
}

PKG_PARAMS_LIST = ["modules", "packages", "features"]

PKG_FILES = {
    filename: None
    for filename in ["doc.txt", "Makefile", "Makefile.dep", "Makefile.include"]
}

PKG_RENAMED_FILES = {"pkg.mk": "{name}.mk"}


def generate_pkg(interactive, config, riotbase):
    """Generate the code of a package."""
    group = "pkg"
    params, output_dir = generate(
        group,
        PKG_PARAMS,
        PKG_PARAMS_LIST,
        PKG_FILES,
        interactive,
        config,
        riotbase,
        in_riot_dir="pkg",
    )

    render_source(params, group, PKG_RENAMED_FILES, output_dir)

    click.echo(
        click.style(
            "Package '{name}' generated in {output_dir} with success!".format(
                name=params[group]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
