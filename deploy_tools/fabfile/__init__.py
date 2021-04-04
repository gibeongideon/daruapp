#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from contextlib import contextmanager as _contextmanager
from fabric.api import run, env, cd, prefix, local
# extra content
from django_commands import makemigrations, migrate, static
# from nginx_commands import supervisor_reset_gunicorn
from supervisor_commands import supervisor_reset_gunicorn
# from ubuntu_commands import *
# from swap_commands import *


env.hosts = ['daruwheel']
env.user = 'root'
env.directory = '/www/daruwheel-pack/daruwheel/'
env.activate = 'source /www/daruwheel-pack/bin/activate'


@_contextmanager
def virtualenv():
    "Activate virtualenv"
    with cd(env.directory):
        with prefix(env.activate):
            yield


def py(context):
    "Execute python command"
    run("python " + context)


def info():
    "Show host name"
    run('uname -a')


def update():
    "Update server content"
    local("git push")
    with cd(env.directory):
        run('git fetch --all')
        run('git reset --hard origin/master')


def pip(*args):
    "Install package on server. Usage: pip:install,easy_thumbnails"
    with virtualenv():
        run("pip " + " ".join(args))


def load_requirements():
    "Install requirements packages"
    with cd(env.directory):
        with virtualenv():
            run("pip install -r deploy/requirements.txt")


def service(*args):
    "Control Services. Usage:start,nginx"
    run("service " + " ".join(args))


def omo():
    "Lava mais branco"
    with cd(env.directory):
        run('find -name "*.pyc" -delete')


def deploy():
    "Update git repository and reset nginx"
    update()
    omo()
    # syncdb()
    makemigrations()
    migrate()
    static()
    supervisor_reset_gunicorn()
