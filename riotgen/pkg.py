"""RIOT pkg generator module."""

import os

import click

from .common import render_file, generate, TEMPLATE_BASE_DIR


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

PKG_FILES = ["doc.txt", "Makefile", "Makefile.dep", "Makefile.include"]


def generate_pkg(interactive, config, riotbase):
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

    name = params[group]["name"]

    template_dir = os.path.join(TEMPLATE_BASE_DIR, group)
    makefile_pkg_out = os.path.join(output_dir, "{}.mk".format(name))
    render_file(params, template_dir, f"{group}.mk.j2", makefile_pkg_out)

    click.echo(
        click.style(
            "Package '{name}' generated in {output_dir} with success!".format(
                name=name, output_dir=output_dir
            ),
            bold=True,
        )
    )
