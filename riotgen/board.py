import logging
import click

logger = logging.getLogger("riotgen.generator.board")


@click.command()
@click.argument('board')
@click.option('--riotbase', '-r', envvar='RIOTBASE')
def board(board, riotbase):
    logger.debug('Generating board support for %s' % board)
    logger.debug('Using RIOTBASE in %s' % riotbase)
