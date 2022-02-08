#! /home/zorgaur/advancedhosters/HiQCom/terminal/bin/python
import click
from dotenv import load_dotenv
from cmd import cmd

load_dotenv()


# TODO: add logs os.mkdir
# TODO: add commands as modules


@click.group()
def main_group():
    pass


@main_group.command(help='Running docker containers for [hipanel, hiapi, hiam] up')
@click.option('-s', '--setup', 'custom_tag', is_flag=True, required=False,
              help='running setup before running up containers')
def dcu(custom_tag):
    if custom_tag:
        cmd.setup.setup(file_name=__file__)

    cmd.dc_up()


@main_group.command(help='Shutting docker containers for [hipanel, hiapi, hiam] down')
def dcd():
    cmd.dc_down()


@main_group.command(help='Migrates database for [hiapi]')
def dcm():
    cmd.dc_migrate()


@main_group.command(help='sets .env variables')
@click.option('-c', '--custom', 'custom_tag', type=str, is_flag=True, default=False, is_eager=True,
              help='sets custom tag for module folders')
def setup(custom_tag):
    cmd.setup.setup(custom_tag, __file__)


@main_group.command(help='runs a test')
@click.argument('test_name')
def run(test_name):
    cmd.run_test(test_name)


if __name__ == '__main__':
    main_group()
