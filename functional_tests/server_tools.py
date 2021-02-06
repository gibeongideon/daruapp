import io
from django.core import management
# from fabric.api import run
# from fabric.context_managers import settings


def create_session_on_server(username): # revisit
    out = io.StringIO()
    management.call_command(
        'create_session', f'--username={username}', stdout=out)
    return out.getvalue()


def reset_database_on_server():  # revisit
    management.call_command('flush', verbosity=0, interactive=False)

# def _get_manage_dot_py(host):
#     return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


# def reset_database(host):
#     manage_dot_py = _get_manage_dot_py(host)
#     with settings(host_string=f'gai@{host}'):
#         run(f'{manage_dot_py} flush --noinput')


# def create_session_on_server(host, username):
#     manage_dot_py = _get_manage_dot_py(host)
#     with settings(host_string=f'gai@{host}'):
#         session_key = run(f'{manage_dot_py} create_session {username}')
#         return session_key.strip()
       
