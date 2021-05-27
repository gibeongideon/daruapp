from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/gibeongideon/daruapp.git'
projectname='daruapp'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'denv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')




def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../denv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.8 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../denv/bin/python manage.py collectstatic --noinput'
        )


def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../denv/bin/python manage.py migrate --noinput'
        )


def deploy():
    site_folder = f'/home/{env.user}/{projectname}'
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    #_update_virtualenv(source_folder)
    #_update_static_files(source_folder)
    #_update_database(source_folder)
