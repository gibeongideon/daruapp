from .base import FunctionalTestCase, wait_to_load
from users.models import User
from selenium.webdriver.common.keys import Keys
from time import sleep


class LoginTestCase(FunctionalTestCase):

    @wait_to_load
    def wait_to_be_logged_in(self):
        # tim = self.browser.find_element_by_css_selector('tim')
        self.browser.find_element_by_link_text('Logout')

    @wait_to_load
    def wait_to_be_logged_out(self):
        # btn = self.browser.find_element_by_css_selector('.btn')
        self.browser.find_element_by_link_text('Signup here')

    def test_can_login(self):

        # [fixture] sample user is registered
        TEST_USERNAME = 'ibeon'
        TEST_EMAIL = 'ibeon@casino.test'
        TEST_PASSWORD = 'QWErtyUI123!#!#'
        User.objects.create_user(username=TEST_USERNAME,
                                 email=TEST_EMAIL,
                                 password=TEST_PASSWORD)

        # John open home page and obviously he is not logged
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out()

        # He clicks 'Sing in' link
        # self.browser.find_element_by_link_text('Login').click()

        # Then he enter account credentials
        self.browser.find_element_by_name('username').send_keys(TEST_USERNAME)
        # sleep(2)
        self.browser.find_element_by_name('password').send_keys(TEST_PASSWORD)
        # sleep(2)
        self.browser.find_element_by_name('password').send_keys(Keys.ENTER)

        # John is logged in
        # self.wait_to_be_logged_in()
