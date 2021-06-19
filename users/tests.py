from django.test import TestCase  # , Client
from django.urls import reverse
from .models import User
from django.http import HttpRequest
from django.template.loader import render_to_string
from .template_views import register
from django.core.exceptions import ValidationError


class UserTestCase(TestCase):
    def setUp(self):
        self.usera = User.objects.create(
            username="0710087634", email="testa@gmail.com", referer_code="ADMIN"
        )
        self.userb = User.objects.create(
            username="254181008768", email="testb@gmail.com", referer_code="ADMIN"
        )
        self.userc = User.objects.create(
            username="181008773", email="testc@gmail.com", referer_code="ADMIN"
        )
        self.userd = User.objects.create(
            username="2548773", email="testd@gmail.com", phone_number="2548773"
        )

    def test_user_creation(self):
        user = User.objects.get(username="0710087634")
        self.assertEqual(user.username, "0710087634")

    def test_user_count(self):
        self.assertEqual(User.objects.count(), 4)

    def test_correct_saved_pone_number(self):
        """test valid mobile number"""

        self.assertEqual(self.usera.phone_number, "254710087634")
        self.assertEqual(self.userb.phone_number, "254181008768")
        self.assertEqual(self.userc.phone_number, "254181008773")
        self.assertEqual(
            self.userd.phone_number, "2548773-invalid_phone_number"
        )  # pone verification later

    def test_catch_invalid_daru_code(self):
        """test if daru code is valid"""
        user_with_invalid_code = User(
            username="725100456", email="usertest@casino22.com", referer_code=""
        )
        with self.assertRaises(ValidationError):
            user_with_invalid_code.save()
            user_with_invalid_code.full_clean()


# class UserCorrecTemplate(TestCase):
#     def test_omepage_returns_correct_html(self):
#         response = self.client.get('/')
#         print('RES',response)
#         self.assertTemplateUsed(response, 'daru_spin.html')


# VIEW TEST


class LoginPageTest(TestCase):

    TEST_USERNAME = "0721399876"
    TEST_EMAIL = "john@casino.test"
    TEST_PASSWORD = "Tw0jaStaraZ4pierdala"

    def test_user_can_login_with_valid_data(self):
        User.objects.create_user(
            username=self.TEST_USERNAME,
            email=self.TEST_EMAIL,
            password=self.TEST_PASSWORD,
        )
        response = self.client.post(
            "/user/login",
            {"username": self.TEST_USERNAME, "password": self.TEST_PASSWORD},
        )
        self.assertRedirects(response, "/")

    # def test_user_cannot_login_with_invalid_password(self):
    #     User.objects.create_user(username=self.TEST_USERNAME,
    #                              email=self.TEST_EMAIL,
    #                              password=self.TEST_PASSWORD)
    #     response = self.client.post('/user/login', {
    #         'username': self.TEST_USERNAME,
    #         'password': (self.TEST_PASSWORD + '34334')
    #     })
    #     print('RESS',response)
    #     self.assertContains(response,
    #                         "Please fill in this field.")
