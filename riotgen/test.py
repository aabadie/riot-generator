import logging
import click

logger = logging.getLogger("riotgen.generator.test")


@click.command()
@click.argument('test')
@click.option('--riotbase', '-r', envvar='RIOTBASE')
@click.option('--modules', '-m', multiple=True)
@click.option('--packages', '-p', multiple=True)
@click.option('--features', '-f', multiple=True)
@click.option('--board', envvar='BOARD', default='native')
def test(test, riotbase, modules, packages, features, board):
    logger.debug('Generating test %s' % test)
    logger.debug('Using modules %s' % ', '.join(modules))
    logger.debug('Using packages %s' % ', '.join(packages))
    logger.debug('Using features %s' % ', '.join(features))
    logger.debug('Targetting board %s' % board)
    logger.debug('Using RIOTBASE in %s' % riotbase)
