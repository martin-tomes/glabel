import click
import configparser
import sys

from .glabel import Glabel

def get_credentials(file):
    """ Derives credentials form an auth file
        :param: a config file with auth keys
        :return: config list with twitter credentials
    """
    lbl.read()
    config = configparser.ConfigParser()
    config.read(file)
    return config['github']['token']

@click.command()
@click.option('-a', '--config-auth', default='./auth.cfg',
                help='File with authorization configuration.', metavar='FILENAME',
                type=click.Path(exists=True))
@click.option('-l', '--config-labels', default='./labels.cfg', metavar='FILENAME',
                type=click.Path(exists=True))
@click.option('-s', '--state', default='open',
                help='Filter pulls by state. [default: open]',
                type=click.Choice(['open', 'closed', 'all']))
@click.option('-b', '--base', help='Filter pulls by base (PR target) branch name.', metavar='BRANCH')
@click.option('d', '--delete-old', default=True, help='Delete labels that do not match anymore.')


def run(config_file):
    """ Run terminal labeler """
    token = get_credentials(config_file)
    lbl = Glabel(token)
    lbl.read()
