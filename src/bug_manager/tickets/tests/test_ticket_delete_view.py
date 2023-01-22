from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Ticket
from ..views.ticket_list_view import TicketListView


class TicketDeleteViewTests(TestCase):

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
        self.delete_path = reverse('tickets:tickets-delete', kwargs={"id": self.ticket.id})

    def test_get_delete_ticket(self):
        """ Successful GET to list delete page """
        response = self.client.get(self.delete_path)
        self.assertEqual(response.status_code, 200)

    def test_delete_ticket(self):
        """ Successful delete ticket """
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 1)
        response = self.client.post(self.delete_path)
        self.assertEqual(response.status_code, 302)
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 0)

    def test_get_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.get(self.delete_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.delete_path}")

    def test_post_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.post(self.delete_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.delete_path}")
