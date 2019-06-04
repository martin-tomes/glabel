import click
import configparser
import sys

def get_credentials(file):
    """ Derives credentials form an auth file
        :param file: a config file with auth keys
        :return: config list with twitter credentials
    """
    config = configparser.ConfigParser()
    config.read(file)

    return config['github']['token']

@click.command()
@click.option('--config_file', default='./auth.cfg',
                help='A path to a configuration file',
                type=click.Path(exists=True))

def run(config_file):
    """ Run terminal labeler """

