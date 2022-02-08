import click

from Helper.Helper import *

setup_log = get_logger(__name__, ' ')


def log_setup_argument(arg=None):
    def log_setup(function):
        def wrapper(*args, **kwargs):
            if arg is None:
                setup_log.info(f'setting up {args[1].upper()}_DIR:')
            else:
                setup_log.info(f'setting up {arg}:')
            function(*args, **kwargs)
            click.echo(click.secho('OK', fg='green'))
        return wrapper
    return log_setup


def setup(tag=None, file_name=None):
    env_file = find_dotenv()
    set_BASH_DIR(env_file, file_name)
    set_WORK_DIR(env_file, file_name)
    set_PREFIX(env_file, tag)
    set_MODULE_DIR(env_file, 'hiapi')
    set_MODULE_DIR(env_file, 'hipanel')


@log_setup_argument('BASH_DIR')
def set_BASH_DIR(env_file, file_name):
    load_dotenv()

    cwd = os.path.realpath(file_name)
    cwd = os.path.split(cwd)[0]
    set_key(env_file, 'BASH_DIR', cwd + '/bash')


@log_setup_argument('WORK_DIR')
def set_WORK_DIR(env_file, file_name):
    load_dotenv()

    cwd = os.path.realpath(file_name)
    cwd = os.path.split(cwd)[0]
    while True:
        cwd, found = walk_through(cwd)
        if not os.path.isdir(cwd):
            error_message(stderr='Unable to found modules folders\n',
                          tip='Ensure script parent folder lays in the directory with modules folders')
            break
        if found:
            set_key(env_file, 'WORK_DIR', cwd)
            break


@log_setup_argument('PREFIX')
def set_PREFIX(env_file, tag):
    load_dotenv()

    if tag is None:
        tag = 'advancedhosters'
    set_key(env_file, 'PREFIX', tag)


@log_setup_argument()
def set_MODULE_DIR(env_file, module_name):
    dir_name = module_name.upper() + '_DIR'
    load_dotenv()
    if os.getenv(dir_name) is not None:
        return
    set_key(env_file, dir_name, str(os.getenv('WORK_DIR')) + '/{}.{}.com'.format(module_name, os.getenv('PREFIX')))
