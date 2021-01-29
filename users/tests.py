from django.test import TestCase  #,Client
from django.urls import reverse
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test_user", email="test@gmail.com")
      
    def test_user_creation(self):

        """Create user """
        user = User.objects.get(username="test_user")
        self.assertEqual(user.username, 'test_user')



    def test_login_returns_correct_html(self):

        response = self.client.get('register')
        
        html = response.content.decode('utf8')
        print(f'resssP{html}')
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.strip().endswith('</html>'))
        # self.assertTemplateUsed(response, 'signup.html')
        self.assertTemplateUsed(response, 'signup.html')

        