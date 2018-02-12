import logging
import click

logger = logging.getLogger("riotgen.generator.driver")


@click.command()
@click.argument('driver')
@click.option('--riotbase', '-r', envvar='RIOTBASE')
@click.option('--dependency', '-d', multiple=True)
def driver(driver, riotbase, dependency):
    logger.debug('Generating driver support for %s' % driver)
    logger.debug('Driver dependencies: %s' % ', '.join(dependency))
    logger.debug('Using RIOTBASE in %s' % riotbase)