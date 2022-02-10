from django.test import TestCase, Client
from django.contrib.auth import get_user_model


# Create your tests here.
User = get_user_model()


class UserRegistrationTest(TestCase):
    """
    Test case for user registration
    """

    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        """
        Test case for user registration
        """
        response = self.client.post('/users/register/', {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'J0hn@d0e',
            'password2': 'J0hn@d0e'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserLoginTest(TestCase):
    """
    Test case for user login
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_login(self):
        """
        Test case for user login
        """
        response = self.client.post('/users/login/', {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
