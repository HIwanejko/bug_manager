from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Ticket


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'ticket_delete.html'

    def get_object(self):
        ticket_id = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=ticket_id)

    @staticmethod
    def get_success_url():
        return reverse('tickets:tickets-list')
