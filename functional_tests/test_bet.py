# from .base import FunctionalTestCase, wait_to_load
# # from unittest.mock import patch
# # from django.utils import timezone
# # from unittest.mock import patch
# from users.models import User
# from selenium.webdriver.support.select import Select

# import time


# class BetTest(FunctionalTestCase):

#     # LOGIN_ERROR = 'You have to be logged!'
#     # OUT_OF_TOKENS = 'You do not have enough tokens!'

#     # @wait
#     # def wait_for_tokens_count(self):
#     #     return self.browser.find_element_by_id('tokens-count')

#     # @wait
#     # def wait_for_exact_tokens_count(self, count):
#     #     element = self.wait_for_tokens_count()
#     #     self.assertEqual(element.text, str(count))

#     # @wait
#     # def wait_to_login_error(self):
#     #     div = self.browser.find_element_by_id('swal2-content')
#     #     self.assertEqual(div.text, self.LOGIN_ERROR)

#     # @wait
#     # def wait_to_out_of_tokens_error(self):
#     #     div = self.browser.find_element_by_id('swal2-content')
#     #     self.assertEqual(div.text, self.OUT_OF_TOKENS)

#     # def close_sweet_modal(self):
#     #     button = self.browser.find_element_by_css_selector(
#     #         'button.swal2-confirm'
#     #     )
#     #     button.click()

#     # @wait
#     # def wait_to_be_logged_out(self):
#     #     navbar = self.browser.find_element_by_css_selector('.navbar')
#     #     navbar.find_element_by_link_text('Sign in')

#     # @wait
#     # def wait_for_bet_buttons(self):
#     #     self.browser.find_element_by_id('bet_green')
#     #     self.browser.find_element_by_id('bet_red')
#     #     self.browser.find_element_by_id('bet_black')

#     def wait_while_wheel_spin(self):
#         time.sleep(15)


#     def test_can_bet(self):

#         self.create_pre_authenticated_session('user')

#         # John open '/roulette' page as logged user
#         self.browser.get(self.live_server_url)

#         self.browser.find_element_by_id('spin_button').click()
#         # self.assertEqual(welcome.text, 'Bet color john!')
#         self.wait_while_wheel_spin()

#         # Now he can click any colored button to bet 1 token
#         # self.browser.find_element_by_id('bet_button').click()

#         # # self.wait_for_exact_tokens_count(4)
#         # time.sleep(3)

#         # self.browser.find_element_by_id('bet_green').click()
#         # self.wait_for_exact_tokens_count(3)

#         # self.browser.find_element_by_id('bet_black').click()
#         # self.wait_for_exact_tokens_count(2)

#         # # Now he decided to increse bet amount
#         # self.browser.find_element_by_name('rates')
#         # self.browser.find_element_by_xpath(
#         #     "//select[@id='rates']/option[2]").click()

#         # self.browser.find_element_by_id('bet_black').click()
#         # self.wait_to_out_of_tokens_error()
#         # self.close_sweet_modal()
