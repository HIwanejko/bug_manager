from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from .views import index_view


class IndexViewTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test_user',
                                             password=self.user_raw_password)
        self.client.login(username=self.user.username, password=self.user_raw_password)
        self.index_path = reverse('index')

    def test_get_detail_ticket(self):
        """ Successful GET to detail page """
        response = self.client.get(self.index_path)
        self.assertEqual(response.status_code, 200)

    def test_get_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.get(self.index_path)
        request.user = AnonymousUser()
        response = index_view(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.index_path}")

    def test_post_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.post(self.index_path)
        request.user = AnonymousUser()
        response = index_view(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.index_path}")
