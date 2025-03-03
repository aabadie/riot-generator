"""RIOT pkg generator module."""

import os

import click

from riotgen.common import (
    check_overwrite,
    load_and_check_params,
    load_license,
    render_source,
)

PKG_PARAMS = {
    "name": {"args": ["Package name"], "kwargs": {}},
    "displayed_name": {
        "args": ["Package displayed name (for doxygen documentation)"],
        "kwargs": {},
    },
    "url": {"args": ["Package source url"], "kwargs": {}},
    "hash": {"args": ["Package version hash"], "kwargs": {}},
    "pkg_license": {"args": ["Package license"], "kwargs": {}},
    "description": {"args": ["Package short description"], "kwargs": {}},
}

PKG_PARAMS_LIST = ["modules", "packages", "features_required"]

PKG_FILES = {
    filename: None
    for filename in ["doc.md", "Makefile", "Makefile.dep", "Makefile.include"]
}

PKG_RENAMED_FILES = {"pkg.mk": "{name}.mk"}


def generate_pkg(interactive, config, riotbase):
    """Generate the code of a package."""
    group = "pkg"
    params = load_and_check_params(
        group,
        PKG_PARAMS,
        PKG_PARAMS_LIST,
        interactive,
        config,
        riotbase,
        "pkg",
    )

    output_dir = os.path.join(riotbase, "pkg", params[group]["name"])
    check_overwrite(output_dir)
    render_source(params, group, PKG_FILES, output_dir)
    render_source(params, group, PKG_RENAMED_FILES, output_dir)

    # Generate the Kconfig file separately because of the different license
    # format
    load_license(params, "# ")
    render_source(params, group, {"Kconfig": None}, output_dir)

    click.echo(
        click.style(
            f"Package '{params[group]['name']}' generated in {output_dir} with success!",
            bold=True,
        )
    )
