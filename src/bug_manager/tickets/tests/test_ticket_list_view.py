from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Ticket
from ..views.ticket_list_view import TicketListView


class TicketListViewTests(TestCase):

    def setUp(self):
        """ Setup test user not super user """
        self.client = Client()
        self.list_path = reverse('tickets:tickets-list')
        self.user_raw_password = "password"
        self.user = User.objects.create_user(username='test_user',
                                             password=self.user_raw_password)
        self.client.login(username=self.user.username, password=self.user_raw_password)

    def test_get_list_view(self):
        """ Successful GET to list view page """
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)

    def test_is_secured(self):
        """ test secured page """
        factory = RequestFactory()
        request = factory.get(self.list_path)
        request.user = AnonymousUser()
        response = TicketListView.as_view()(request)
        # Redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login?next=/tickets/")

    def test_no_tickets_are_displayed(self):
        """ Successful GET to list view page with no tickets """
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['ticket_list'], [])

    def test_tickets_are_displayed(self):
        """ Successful GET to list view page with tickets """
        ticket = Ticket.objects.create(name='Test Ticket',
                                            description='Test Description',
                                            status="Open",
                                            assigned_to="Unassigned",
                                            created_by=self.user)
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['ticket_list'], [ticket])
