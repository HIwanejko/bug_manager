from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Ticket


class TicketListView(LoginRequiredMixin, ListView):
    template_name = 'ticket_list.html'
    queryset = Ticket.objects.all()
    context_object_name = 'ticket_list'
