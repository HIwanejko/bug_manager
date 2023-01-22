from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Ticket
from ..views.ticket_list_view import TicketListView


class TicketUpdateViewTests(TestCase):

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
        self.update_path = reverse('tickets:tickets-update', kwargs={"id": self.ticket.id})

    def test_get_update_ticket(self):
        """ Successful GET to update page """
        response = self.client.get(self.update_path)
        self.assertEqual(response.status_code, 200)

    def test_update_ticket(self):
        """ Successful update ticket """
        # Initial Ticket
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 1)
        created_ticket = tickets[0]
        self.assertEqual(created_ticket.name, "Test Ticket")
        self.assertEqual(created_ticket.description, "Test Description")
        self.assertEqual(created_ticket.status, 'Open')
        self.assertEqual(created_ticket.assigned_to, 'Unassigned')
        self.assertEqual(created_ticket.created_by, self.user.username)
        # Update Ticket
        data = {
            "name": 'Test Ticket 2',
            "description": "Changed",
            "status": "Closed",
            "assigned_to": self.ticket.assigned_to
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 1)
        updated_ticket = tickets[0]
        self.assertEqual(updated_ticket.name, "Test Ticket 2")
        self.assertEqual(updated_ticket.description, "Changed")
        self.assertEqual(updated_ticket.status, 'Closed')
        self.assertEqual(updated_ticket.assigned_to, 'Unassigned')
        self.assertEqual(updated_ticket.created_by, self.user.username)

    def test_get_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.get(self.update_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.update_path}")

    def test_post_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.post(self.update_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/auth/login?next={self.update_path}")
