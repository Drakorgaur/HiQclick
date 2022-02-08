import os
import click
from dotenv import *
import subprocess
import logging
from time import sleep


def get_logger(name, terminator='\n'):
    logger = logging.getLogger(name)
    cHandle = logging.StreamHandler()
    cHandle.terminator = terminator
    cHandle.setFormatter(logging.Formatter(fmt='%(levelname)s [ %(asctime)s ] %(message)s', datefmt="%H:%M:%S"))
    logger.addHandler(cHandle)
    logger.setLevel(logging.INFO)
    return logger


load_dotenv()
log = get_logger(__name__)


def run_script(script_name, args=None, cwd=os.getenv('BASH_DIR'), split='\n', stdout=subprocess.PIPE,
               stderr=subprocess.DEVNULL):
    script = [script_name]
    for item in args:
        script.append(item)
    sp = subprocess.Popen(script, cwd=cwd, stdout=stdout, stderr=stderr, encoding='utf-8',)
    response, _ = sp.communicate()
    if response:
        return split_stdout(response, split)


def error_message(stderr, tip=None):
    click.echo(click.style('Error occurred:', fg='red'))
    log.error(stderr)
    if tip is not None:
        click.echo(click.style('Tip:', fg='yellow'))
        log.info(tip)


def wait_for_env_updates(var, time=20):
    """
    waits $time secs until .env gets variable with $var key
    """
    for i in range(time):
        load_dotenv()
        if os.getenv(var) is None:
            sleep(1)
        else:
            return True
    error_message('.env didnt get a {} variable'.format(var))
    return False


def get_dirs(cwd):
    # TODO: rework with run_script
    cml = ''

    for item in ['ls', '|', 'grep', "'{}'".format(os.getenv('PREFIX'))]:
        cml += item + ' '
    sp = subprocess.run(cml, shell=True, capture_output=True, cwd=cwd, universal_newlines=True)
    if not sp:
        error_message(stderr='Error: hipanel, hiam and hiapi folders were not found',
                      tip='Ensure script parent folder lays in the directory with modules folders')

    return sp.stdout.splitlines()


def get_folders_cwd():
    """
    Method checks if hipanel, hiapi and hiam folders exist
    """
    cwd = os.getenv('WORK_DIR')
    if not cwd:
        error_message(stderr='environmental variable WORK_DIR is not set\n',
                      tip='run \'setup\' command to set it and other needed variables up')
        return None

    directories = get_dirs(cwd)

    for module in ['hipanel', 'hiapi', 'hiam']:
        found = False
        for directory in directories:
            if module in directory:
                found = True
                break
        if not found:
            print('module-dir {} was not found'.format(module))
            return None

    return cwd


def walk_through(cwd):
    modules = {
        'hipanel': False,
        'hiapi': False,
        'hiam': False,
    }
    cwd = os.path.split(cwd)[0]
    if not wait_for_env_updates('BASH_DIR'):
        return '', False
    sp = subprocess.Popen(['./ls.sh', cwd], stdout=subprocess.PIPE, encoding='utf-8', cwd=os.getenv('BASH_DIR'))
    output, _ = sp.communicate()
    output = output.split('\n')
    for line in output:
        for module in modules:
            if module in line:
                modules[module] = True
    for module in modules:
        if modules[module] is False:
            return cwd, False
    return cwd, True


def check_module_running(module):
    print('Checking {} is running: '.format(module), end='')
    cmd = module.lower() + ' -v'
    sp = subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)

    if module + ' version' in sp.stdout:
        click.echo(click.style('OK', fg='green'))
        return True
    click.echo(click.style('Fail', fg='green'))
    return False


def split_stdout(output, split='\n'):
    result = output.split(split)
    if len(result) > 1:
        del result[-1]
    return result