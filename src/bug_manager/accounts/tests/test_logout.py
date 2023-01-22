from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LogoutTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.logout_path = reverse('accounts:logout')
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test_user',
                                             password=self.user_raw_password)

    def test_get_method_not_used(self):
        """not allowed response from get to logout"""
        response = self.client.get(self.logout_path)
        self.assertEqual(response.status_code, 405)

    def test_post_logged_in_user(self):
        """logged in user logged out and session removed"""
        self.client.login(username=self.user.username, password=self.user_raw_password)
        response = self.client.post(self.logout_path, follow=True)
        self.assertRedirects(response, '/auth/login/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_post_not_logged_in_user(self):
        """not logged in user attempt log out"""
        response = self.client.post(self.logout_path, follow=True)
        self.assertEqual(response.status_code, 401)
