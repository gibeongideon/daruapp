from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    SESSION_KEY,
    HASH_SESSION_KEY,
    get_user_model,
)
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            dest="username",
            help="Username for creating pre-authenticated session",
            required=True,
        )

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options["username"],)
        self.stdout.write(session_key, ending="")


def create_pre_authenticated_session(username):
    user = User.objects.create(username=username)
    session = SessionStore(None)
    session.clear()
    session.cycle_key()
    session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key
