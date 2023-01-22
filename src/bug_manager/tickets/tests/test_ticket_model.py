from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Ticket


class TicketModelTests(TestCase):

    def setUp(self):
        """Setup test user"""
        self.user = User.objects.create_user(username='test',
                                             password='password')

    def test_ticket_model(self):
        """Ticket is created with correct attributes"""
        ticket = Ticket.objects.create(name='Test Ticket',
                                       description='Test Description',
                                       status="Open",
                                       assigned_to="Unassigned",
                                       created_by=self.user)
        self.assertEqual(ticket.name, 'Test Ticket')
        self.assertEqual(ticket.description, 'Test Description')
        self.assertEqual(ticket.status, "Open")
        self.assertEqual(ticket.assigned_to, "Unassigned")
        self.assertEqual(ticket.created_by.username, 'test')
        self.assertNotEqual(ticket.created_by.password, 'password')
