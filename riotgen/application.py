"""RIOT application generator module."""

import os.path
import datetime

import click

from .helpers import _get_usermail, _get_username
from .helpers import TEMPLATES_DIR
from .helpers import _read_config, _prompt_common_information


def _read_application_config(filename):
    return _read_config(filename, section='application')


def _prompt_application():
    params = {}
    params['application_name'] = click.prompt(text='Application name')
    params['desc'] = click.prompt(text='Application short description')
    params['board'] = click.prompt(text='Target board', default='native')
    params['modules'] = click.prompt(
        text='Required modules (comma separated)',
        default=[], type=list)
    params['packages'] = click.prompt(
        text='Required packages (comma separated)',
        default=[], type=list)
    params['features'] = click.prompt(
        text='Required board features (comma separated)',
        default=[], type=list)

    params.update(_prompt_common_information())
    return params


def _check_params(params):
    return dict()


@click.command()
@click.argument('output_dir', type=click.Path(exists=True))
@click.option('--config', type=click.File(mode='r'))
def application(output_dir, config):
    # click.echo('Generating application: ', nl=False)
    # click.echo(click.style('{}'.format(application), bold=True))
    # click.echo('Target board: ', nl=False)
    # click.echo(click.style('{}'.format(board), bold=True))

    # Use config file is set
    if config is not None:
        params = _read_application_config(config)
    else:
        params = _prompt_application()

    print(params)

    includes = ''
    # Modules required
    # if modules:
    #     click.echo('Modules: ', nl=False)
    #     click.echo(click.style(', '.join(modules), bold=True))
    #     for module in modules:
    #         includes += 'USEMODULE += {}\n'.format(module)

    # # External packages required
    # if packages:
    #     click.echo('Packages: ', nl=False)
    #     click.echo(click.style(', '.join(packages), bold=True))
    #     for pkg in packages:
    #         includes += 'USEPKG += {}\n'.format(pkg)

    # # Board/CPU features required
    # if features:
    #     click.echo('Features: ', nl=False)
    #     click.echo(click.style(', '.join(features), bold=True))
    #     for feature in features:
    #         includes += 'FEATURES_REQUIRED += {}\n'.format(feature)

    # User name
    username = _get_username()
    click.echo('Username: ', nl=False)
    click.echo(click.style(username, bold=True))

    # User email
    usermail = _get_usermail()
    click.echo('Email: ', nl=False)
    click.echo(click.style(usermail, bold=True))

    # params = dict(
    #     application_name=application_name,
    #     application_name_underline='=' * len(application_name),
    #     board=board,
    #     year=datetime.datetime.now().year,
    #     # organization=organization if organization is not None else username,
    #     # desc=description,
    #     author_name=username,
    #     author_email=usermail,
    #     includes=includes,
    # )

    application_dir = os.path.join(TEMPLATES_DIR, 'application')
    main_in = os.path.join(application_dir, 'main.c')
    makefile_in = os.path.join(application_dir, 'Makefile')
    readme_in = os.path.join(application_dir, 'README.md')
    main_out = os.path.join(output_dir, 'main.c')
    makefile_out = os.path.join(output_dir, 'Makefile')
    readme_out = os.path.join(output_dir, 'README.md')

    files = {
        main_in: main_out,
        makefile_in: makefile_out,
        readme_in: readme_out
    }

    for file_in, file_out in files.items():
        with open(file_in, 'r') as f_in:
            with open(file_out, 'w') as f_out:
                f_out.write(f_in.read().format(**params))    

    click.echo(click.style('Application generated!', bold=True))
