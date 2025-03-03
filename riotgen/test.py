"""RIOT test generator module."""

import os

import click

from riotgen.application import (
    get_output_dir,
    load_and_check_application_params,
    render_application_source,
)
from riotgen.common import check_overwrite, load_license, render_source


def generate_test(interactive, config, riotbase):
    """Generate the code of a test application."""
    group = "application"
    params = load_and_check_application_params(
        group,
        interactive,
        config,
        riotbase,
        in_riot_dir="tests",
        testrunner=True,
    )

    params["application"]["type"] = "test"

    output_dir = get_output_dir(params, group, riotbase, "tests")
    check_overwrite(output_dir)

    render_application_source(params, group, output_dir)

    test_params = params[group]
    if "use_testrunner" in test_params and test_params["use_testrunner"] in (
        True,
        "True",
        "y",
    ):
        load_license(params, "# ")
        testrunner_dir = os.path.join(output_dir, "tests")
        render_source(params, group, {"01-run.py": None}, testrunner_dir)
        os.chmod(os.path.join(testrunner_dir, "01-run.py"), 0o755)

    click.echo(
        click.style(
            f"Test '{params[group]['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
