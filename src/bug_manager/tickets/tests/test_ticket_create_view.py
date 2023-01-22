from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Ticket
from ..views.ticket_list_view import TicketListView


class TicketCreateViewTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.create_path = reverse('tickets:tickets-create')
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test_user',
                                             password=self.user_raw_password)
        self.client.login(username=self.user.username, password=self.user_raw_password)

    def test_get_create_ticket(self):
        """ Successful GET to list create page """
        response = self.client.get(self.create_path)
        self.assertEqual(response.status_code, 200)

    def test_get_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.get(self.create_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login?next=/tickets/create/")

    def test_post_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.post(self.create_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login?next=/tickets/create/")

    def test_post_create_ticket(self):
        """ test success on post request """
        data = {
            "name": 'Test Ticket',
            "description": 'Description',
            "status": 'Open',
            "assigned_to": 'Unassigned'
        }
        response = self.client.post(self.create_path, data=data)
        self.assertEqual(response.status_code, 302)
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 1)
        created_ticket = tickets[0]
        self.assertEqual(created_ticket.name, "Test Ticket")
        self.assertEqual(created_ticket.description, "Description")
        self.assertEqual(created_ticket.status, "Open")
        self.assertEqual(created_ticket.assigned_to, "Unassigned")
        self.assertEqual(created_ticket.created_by, self.user.username)
        self.assertRedirects(response, f'/tickets/{created_ticket.id}/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_post_created_by_field_not_overridable(self):
        """ test success on post request with extra field provided """
        data = {
            "name": 'Test Ticket',
            "description": 'Description',
            "status": 'Open',
            "assigned_to": 'Unassigned',
            "created_by": "overridden"
        }
        self.client.post(self.create_path, data=data)
        tickets = Ticket.objects.all()
        self.assertEqual(len(tickets), 1)
        created_ticket = tickets[0]
        self.assertEqual(created_ticket.name, "Test Ticket")
        self.assertEqual(created_ticket.description, "Description")
        self.assertEqual(created_ticket.status, "Open")
        self.assertEqual(created_ticket.assigned_to, "Unassigned")
        self.assertEqual(created_ticket.created_by, self.user.username)

    def test_ticket_name_required(self):
        """ Failure on creation with missing name """
        data = {
            "description": 'Description',
            "points": 1,
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_ticket_description_required(self):
        """ Failure on creation with missing description """
        data = {
            "name": 'Test Ticket',
            "points": 1,
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_ticket_name_invalid(self):
        """ Failure on creation with invalid name """
        data = {
            "name": '!nvalid',
            "description": 'Description',
            "points": 1,
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "Your Ticket name must only contain A-z and 0-9 and white space", status_code=400)

    def test_ticket_description_invalid(self):
        """ Failure on creation with invalid description """
        data = {
            "name": 'Test Ticket',
            "description": '!nvalid',
            "points": 1,
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "Your Ticket description must only contain A-z and 0-9 and white space",
                            status_code=400)

    def test_ticket_description_too_long(self):
        """ Failure on creation with too long description"""
        data = {
            "name": 'Test Ticket',
            "description": "A" * 301,
            "points": 1,
        }
        response = self.client.post(self.create_path, data=data)
        self.assertContains(response, "Ensure this value has at most 300 characters (it has 301).", status_code=400)
