import configparser
import click
import asyncio

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
@click.option('-a', '--config-auth',
              default='./auth.cfg',
              help='File with authorization configuration.',
              metavar='FILENAME',
              type=click.Path(exists=True))
@click.option('-c', '--config-labels',
              default='./config.cfg',
              help='File with labels configuration',
              metavar='FILENAME',
              type=click.Path(exists=True))
@click.option('-s', '--state',
              default='open',
              help='Filter pulls by state. [default: open]',
              type=click.Choice(['open', 'closed', 'all']),
              required=False)
@click.option('-b', '--base',
              default='master',
              help='Filter pulls by base (PR target) branch name.',
              metavar='BRANCH',
              required=False)
@click.option('-d', '--delete-old',
              default=True,
              is_flag=True,
              show_default=True,
              help='Delete labels that do not match anymore.')
@click.option('-D', '--delete-all',
              default=False,
             # is_flag=True,
              show_default=True,
              help='Delete all labels from reposlugs.')
@click.argument('reposlugs', nargs=-1, required=False)
def run(config_auth, config_labels, state, base, delete_old, delete_all, reposlugs):
    """ Run terminal labeler """
    token = get_credentials(config_auth)
    lbl = Glabel(token, config_labels, reposlugs, delete_all, state, base)
    asyncio.run(lbl.run())


# async def main(token, config_labels, reposlugs, delete_all):
#     lbl = Glabel(token, config_labels, reposlugs, delete_all)

#     try:
#         await lbl.run()
#     finally:
#         await lbl.close()
