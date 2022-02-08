import os
import subprocess

from Helper.Helper import *
from Helper import setup
import re

load_dotenv()
HIAPI_DIR = os.getenv('HIAPI_DIR')
BASH_DIR = os.getenv('BASH_DIR')

log = setup.get_logger(__name__, ' ')


def pre_run(find=None):
    if find is None:
        find = ['', ]
    cwd = get_folders_cwd()
    if cwd is None:
        return None
    check_modules()
    dirs = []
    for directory in get_dirs(cwd):
        for element in find:
            if element in directory:
                dirs.append(f'{cwd}/{directory}')
    return dirs


def grep(ls, find):
    # TODO: rework with run_script
    grep = subprocess.Popen(['grep', find], stdin=ls.stdout, stdout=subprocess.PIPE, encoding='utf-8')
    ls.stdout.close()
    output, _ = grep.communicate()
    python_processes = output.split('\n')
    return python_processes[0]


def check_service(service, error):
    log.info('Checking if %s service is working well:' % service)

    url = f"{service}.{os.getenv('PREFIX')}.com"
    answers = run_script('./curl.sh', [url, error])
    return answers


def kill_nginx():
    line = run_script('./d_ps.sh')
    container = line[0]
    line = run_script('./d_rm.sh', [container])
    if line[0] == container:
        return True
    return False


def set_up_nginx():
    error = 'Bind for 0.0.0.0:80 failed'
    sp = subprocess.Popen(['./d_nginx.sh'], cwd=BASH_DIR,
                          stdout=subprocess.PIPE, encoding='utf-8')
    out, _ = sp.communicate()
    line = split_stdout(out)
    for response in line:
        if error in response:
            error_message(error, 'kill service that listening port 80')
            return False
    return True


def check_nginx():
    responses = check_service('hipanel', 'Welcome to nginx')
    if responses:
        for response in responses:
            if 'Welcome to nginx' in response:
                click.echo(click.style('FAIL', fg='red'))
                log.info('Killing previous nginx master container:')
                if kill_nginx():
                    click.echo(click.style('OK', fg='green'))
                    log.info('Binding port 80 with nginx master container:')
                    if set_up_nginx():
                        click.echo(click.style('OK', fg='green'))
                        break
                    click.echo(click.style('FAIL', fg='red'))
                    error_message('Failed to set up nginx to port 80')
                break
            else:
                break
    click.echo(click.style('OK', fg='green'))


def check_hiapi():
    log.info('Checking if Hiapi was upped successfully:')
    error = '503 Service Temporarily Unavailable'
    ls = subprocess.Popen(['cat', '/etc/hosts'], stdout=subprocess.PIPE)
    url = re.sub(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\s+)([A-z.]+)$", r'\3', grep(ls, 'hiapi'))
    answers = run_script('./curl.sh', [url, error])
    for answer in answers:
        if error in answer:
            click.echo(click.style('FAIL', fg='red'))
            if dc_up('hiapi'):
                log.info('Re-up hiapi container:')
                click.echo(click.style('OK', fg='green'))
                break
        else:
            click.echo(click.style('OK', fg='green'))
            break


def dc_up(folder=None):
    if folder is not None:
        run_script('./dc_up.sh', [HIAPI_DIR])
        return True

    dirs = pre_run()
    if dirs is None:
        return
    for dir in dirs:
        log.info('Upping {}:'.format(re.sub(r'^(.+)(hi[apinelm]{2,5})(.+)$', r'\2', dir)))
        run_script('./dc_up.sh', [dir])
        click.echo(click.style('OK', fg='green'))
    check_nginx()
    check_hiapi()


def dc_down():
    dirs = pre_run()
    if dirs is None:
        return
    for dir in dirs:
        log.info('Shutting down {} :'.format(re.sub(r'^(.+)(hi[apinelm]{2,5})(.+)$', r'\2', dir)))
        run_script('./dc_down.sh', [dir])
        click.echo(click.style('OK', fg='green'))


def check_modules():
    for module in ['Docker', 'docker-compose']:
        check_module_running(module)


def dc_migrate():
    subprocess.run(['./dc_migrate.sh', HIAPI_DIR], cwd=BASH_DIR,
                   stdout=subprocess.DEVNULL, input='yes', encoding='ascii')
    click.echo(click.style('OK', fg='green'))


def find_test(path, test_name):
    if run_script('./ls.sh', [path, test_name]):
        return True


def check_test_name(test_name):
    if 'Cest' in test_name:
        if 'Cest.php' in test_name:
            return test_name
        test_name = test_name + '.php'
        return test_name

    return test_name + 'Cest.php'


def run_test(test_name):
    test_name = check_test_name(test_name)
    print(test_name)
    found_tests = dict()
    variant = 1
    docker_path = '/vendor/hiqdev'
    main_path = os.getenv('HIPANEL_DIR') + docker_path
    modules = run_script('./ls.sh', [main_path, 'hipanel-module-'])
    for module in modules:
        """
        Check for Common test
        """
        module_path = f'{main_path}/{module}/tests/acceptance'
        module = (re.sub(r'^(hipanel-module-)([A-z]+)$', r'\2', module))
        if find_test(module_path, test_name):
            found_tests[variant] = f'hipanel-module-{module}/tests/acceptance/'
            variant += 1

        # TODO: create cycle for all directories while {lsd(path) -> path = new_path}

        folders = run_script('./lsd.sh', [module_path])
        if folders:
            for folder in folders:
                role_path = f'{module_path}/{folder}'

                if find_test(role_path, test_name):
                    found_tests[variant] = f'hipanel-module-{module}/tests/acceptance/{folder}'
                    variant += 1

    if len(found_tests) == 0:
        error_message('Test not found')
    elif len(found_tests) == 1:
        run_script('./run.sh', [os.getenv('HIPANEL_DIR'), f'.{docker_path}/{found_tests[1]}{test_name}'], stdout=None)
    else:
        for var in found_tests:
            print(f'{var}. {found_tests[var]}')
        length = len(found_tests)
        point = 0
        while point == 0:
            print('Choose execution path:', end=' ')
            try:
                point = int(input())
            except ValueError:
                print(f'Enter number from 1 to {length}')

        run_script('./run.sh', [os.getenv('HIPANEL_DIR'), f'.{docker_path}/{found_tests[point]}/{test_name}'],
                   stdout=None)
