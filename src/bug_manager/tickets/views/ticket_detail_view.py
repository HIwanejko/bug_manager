from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Ticket


class TicketDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ticket_detail.html'

    def get_object(self):
        ticket_id = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=ticket_id)
