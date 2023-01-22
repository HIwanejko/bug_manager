from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Ticket
from ..views.ticket_list_view import TicketListView


class TicketDetailViewTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test_user',
                                             password=self.user_raw_password)
        self.client.login(username=self.user.username, password=self.user_raw_password)
        self.ticket = Ticket.objects.create(name='Test Ticket',
                                            description='Test Description',
                                            status="Open",
                                            assigned_to="Unassigned",
                                            created_by=self.user)
        self.detail_path = reverse('tickets:tickets-detail', kwargs={"id": self.ticket.id})

    def test_get_detail_ticket(self):
        """ Successful GET to detail page """
        response = self.client.get(self.detail_path)

        self.assertContains(response, self.ticket.name)
        self.assertContains(response, self.ticket.description)
        self.assertContains(response, self.ticket.status)
        self.assertContains(response, self.ticket.assigned_to)
        self.assertContains(response, self.ticket.created_by)

    def test_get_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.get(self.detail_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.detail_path}")

    def test_post_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.post(self.detail_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.detail_path}")
