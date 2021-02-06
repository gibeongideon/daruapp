from django.test import TestCase  #, Client
from django.urls import reverse
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.usera = User.objects.create(
            username="test_usera", email="testa@gmail.com",
            phone_number="254710087634")
        self.userb = User.objects.create(
            username="test_userb", email="testb@gmail.com",
            phone_number="0181008768")
        self.userc = User.objects.create(
            username="test_userc", email="testc@gmail.com",
            phone_number=181008773)
        self.userd = User.objects.create(
            username="test_userd", email="testd@gmail.com",
            phone_number="2548773")

    def test_user_creation(self):
        user = User.objects.get(username="test_usera")
        self.assertEqual(user.username, 'test_usera')

    def test_user_count(self):
        self.assertEqual(User.objects.count(), 4)

    def test_correct_saved_pone_number(self):

        self.assertEqual(self.usera.phone_number, "254710087634")
        self.assertEqual(self.userb.phone_number, "254181008768")
        self.assertEqual(self.userc.phone_number, "254181008773")
        self.assertEqual(self.userd.phone_number, "2548773invalid")# pone verification later
       