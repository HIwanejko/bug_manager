from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Ticket
from ..forms import TicketModelForm


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'ticket_update.html'
    form_class = TicketModelForm

    def get_object(self):
        ticket_id = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=ticket_id)

    def form_valid(self, form):
        """
        Save user that created the ticket into the model so no overwrite
        """
        ticket = Ticket.objects.get(id=form.instance.id)
        form.instance.created_by = ticket.created_by
        return super(TicketUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Return Bad Request response if form is invalid
        """
        response = super().form_invalid(form)
        response.status_code = 400
        return response
