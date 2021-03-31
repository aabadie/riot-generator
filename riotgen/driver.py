"""RIOT application generator module."""

import os
import click

from .common import load_and_check_params, check_overwrite, render_source, load_license


DRIVER_PARENTS = [
    "actuators",
    "display",
    "can",
    "misc",
    "mtd",
    "netdev",
    "power",
    "sensors",
    "storage",
]

DRIVER_PARAMS = {
    "name": {"args": ["Driver name"], "kwargs": {}},
    "displayed_name": {
        "args": ["Driver Doxygen group name"],
        "kwargs": {},
    },
    "brief": {"args": ["Brief doxygen description"], "kwargs": {}},
    "ingroup": {
        "args": ["Parent driver Doxygen group"],
        "kwargs": {
            "param_type": click.Choice(DRIVER_PARENTS),
            "show_choices": True,
        },
    },
}

DRIVER_FILES = {
    "driver.c": "{name}.c",
    "Makefile": None,
    "Makefile.include": None,
    "Makefile.dep": None,
}

DRIVER_PARAMS_LIST = ["modules", "packages", "features_required"]

DRIVER_INCLUDE_FILES = {"driver.h": "{name}.h"}

DRIVER_INTERNAL_INCLUDE_FILES = {
    "driver_constants.h": "{name}_constants.h",
    "driver_params.h": "{name}_params.h",
}

DRIVER_NETDEV_FILES = {
    "driver_netdev.c": "{name}_netdev.c",
}

DRIVER_NETDEV_INCLUDE_FILES = {
    "driver_netdev.h": "{name}_netdev.h",
}


def generate_driver(interactive, config, riotbase):
    """Generate the code for a driver module."""
    group = "driver"
    params = load_and_check_params(
        group,
        DRIVER_PARAMS,
        DRIVER_PARAMS_LIST,
        interactive,
        config,
        riotbase,
        "drivers",
    )

    drivers_dir = os.path.join(riotbase, "drivers")
    drivers_include_dir = os.path.join(drivers_dir, "include")
    output_dir = os.path.join(drivers_dir, params[group]["name"])
    drivers_internal_include_dir = os.path.join(output_dir, "include")
    check_overwrite(output_dir)
    render_source(params, group, DRIVER_FILES, output_dir)
    render_source(params, group, DRIVER_INCLUDE_FILES, drivers_include_dir)
    render_source(
        params, group, DRIVER_INTERNAL_INCLUDE_FILES, drivers_internal_include_dir
    )

    if params[group]["ingroup"] == "netdev":
        render_source(params, group, DRIVER_NETDEV_FILES, output_dir)
        render_source(
            params, group, DRIVER_NETDEV_INCLUDE_FILES, drivers_internal_include_dir
        )

    # Generate the Kconfig file separately because of the different license
    # format
    load_license(params, "# ")
    render_source(params, group, {"Kconfig": None}, output_dir)

    click.echo(
        click.style(
            f"Driver '{params[group]['name']}' generated in {output_dir} with success!",
            bold=True,
        )
    )
