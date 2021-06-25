import os
import time

# import pytest

import io
from django.core import management
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# from .server_tools import reset_database ,create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

executable_path = "/home/gai/Desktop/Dev/tdd_python/geckodriver"
MAX_WAIT = 10


def create_session_on_server(username):  # revisit
    out = io.StringIO()
    management.call_command("create_session", f"--username={username}", stdout=out)
    return out.getvalue()


def reset_database_on_server():  # revisit
    management.call_command("flush", verbosity=0, interactive=False)


def get_staging_server():  # revisit
    server = os.environ.get("STAGING_SERVER")
    return server


def wait_to_load(fn):
    """wait webdriver to load page """

    def deco_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return deco_fn


class FunctionalTestCase(StaticLiveServerTestCase):
    def setUp(self):

        self.live_server_url = get_staging_server()
        # if not self.live_server_url:
        #     pytest.exit('Now running functional tests in only possible '
        #                 'with staging server')

        # Reset database
        reset_database_on_server()
        # Run browser
        self.browser = webdriver.Firefox(executable_path=executable_path)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def create_pre_authenticated_session(self, username):
        self.staging_server = get_staging_server()
        if self.staging_server:
            # functional tests -> against real server
            session_key = create_session_on_server(username)  # revisit
        else:
            # unit tests -> against fake server
            session_key = create_pre_authenticated_session(username)

        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")

        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/",)
        )
