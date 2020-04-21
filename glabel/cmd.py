import click
import configparser
import sys

from .glabel import Glabel


def get_credentials(file):
    """ Derives credentials form an auth file
        :param: a config file with auth keys
        :return: config list with twitter credentials
    """
    config = configparser.ConfigParser()
    config.read(file)
    return config['github']['token']


@click.command()
@click.option('-a', '--auth', default='./auth.cfg',
              help='File with authorization configuration.', metavar='FILENAME',
              type=click.Path(exists=True))
@click.option('-c', '--config', default='./config.cfg', metavar='FILENAME',
              type=click.Path(exists=True))
@click.option('-s', '--state', default='open', help='Filter pulls by state. [default: open]',
              type=click.Choice(['open', 'closed', 'all']), required=False)
@click.option('-b', '--base', default='master', help='Filter pulls by base (PR target) branch name.',
              metavar='BRANCH', required=False)
@click.option('-d', '--delete-old', default=True, help='Delete labels that do not match anymore.',
              required=False)
@click.argument('reposlugs', nargs=-1, required=False)

def run(auth, config, state, base, delete_old, reposlugs):
    """ Run terminal labeler """
    token = get_credentials(auth)
    lbl = Glabel(token, config, reposlugs)
    print(lbl.read_repo())
