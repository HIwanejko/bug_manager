from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.register_path = reverse('accounts:register')
        self.admin_path = "/admin/"

    def test_get_register_page(self):
        """ Test successful GET to register page """
        response = self.client.get(self.register_path)
        self.assertEqual(response.status_code, 200)

    def test_post_register_page(self):
        """ Test successful POST to register page and user created """
        username = "test"
        password = "Really!SecurePassword1"
        data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        user = User.objects.get(username=username)
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password, password)

    def test_post_empty_username(self):
        """ Test invalid register attempt with empty username """
        password = "Really!SecurePassword1"
        data = {
            "username": '',
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_empty_password1(self):
        """ Test invalid register attempt with empty password1 """
        username = "test"
        password = "Really!SecurePassword1"
        data = {
            "username": username,
            "password1": '',
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_empty_password2(self):
        """ Test invalid register attempt with empty password2 """
        username = "test"
        password = "Really!SecurePassword1"
        data = {
            "username": username,
            "password1": password,
            "password2": ""
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_missing_username(self):
        """ Test invalid register attempt with missing username field """
        password = "Really!SecurePassword1"
        data = {
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_missing_password1(self):
        """ Test invalid register attempt with missing password1 """
        username = "test"
        password = "Really!SecurePassword1"
        data = {
            "username": username,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_missing_password2(self):
        """ Test invalid register attempt with missing password2 """
        username = "test"
        password = "Really!SecurePassword1"
        data = {
            "username": username,
            "password1": password,
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This field is required.", status_code=401)

    def test_post_invalid_username(self):
        """ Test invalid register attempt with invalid username """
        password = "Really!SecurePassword1"
        data = {
            "username": '!nval1d#',
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response,
                            "Enter a valid username. This value may contain only letters, "
                            "numbers, and @/./+/-/_ characters.",
                            status_code=401)

    def test_post_invalid_password(self):
        """ Test invalid register attempt with invalid password """
        username = 'test'
        password = "password"
        data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "This password is too common.", status_code=401)

    def test_post_register_with_same_username(self):
        """ Test invalid register attempt with same username """
        username = 'test'
        password = "Really!SecurePassword1"
        data = {
            "username": username,
            "password1": password,
            "password2": password
        }
        response = self.client.post(self.register_path, data=data)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertIsNotNone(User.objects.get(username=username))
        self.client.logout()
        # Register 2nd user with same details
        response = self.client.post(self.register_path, data=data)
        self.assertContains(response, "A user with that username already exists.", status_code=401)
