from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.login_path = reverse('accounts:login')
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test_user',
                                             password=self.user_raw_password)

    def test_get_happy_path_login(self):
        """Successful login page"""
        response = self.client.get(self.login_path)
        self.assertEqual(response.status_code, 200)

    def test_post_happy_path_user_login(self):
        """Successful login attempt"""
        data = {
            "username": self.user.username,
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        # Verify session is created and redirected
        self.assertTrue(response.client.cookies.get('sessionid') is not None)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_login_empty_username(self):
        """Unsuccessful login attempt with empty username"""
        data = {
            "username": '',
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_login_empty_password(self):
        """Unsuccessful login attempt with empty password"""
        data = {
            "username": self.user.username,
            "password": ''
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_login_missing_username(self):
        """Unsuccessful login attempt with missing username"""
        data = {
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_login_missing_password(self):
        """Unsuccessful login attempt with missing username"""
        data = {
            "username": self.user.username,
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_login_invalid_username(self):
        """Unsuccessful login attempt with invalid username"""
        data = {
            "username": 'invalid£#user!name',
            "password": self.user_raw_password
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response,
                            "Please enter a correct username and password. "
                            "Note that both fields may be case-sensitive.",
                            status_code=401)

    def test_login_invalid_password(self):
        """Unsuccessful login attempt with invalid password"""
        data = {
            "password": self.user.username,
            "username": 'invalid£#password'
        }
        response = self.client.post(self.login_path, data=data, follow=True)
        self.assertContains(response,
                            "Please enter a correct username and password. "
                            "Note that both fields may be case-sensitive.",
                            status_code=401)
