from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Ticket
from ..forms import TicketModelForm


class TicketCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ticket_create.html'
    form_class = TicketModelForm
    queryset = Ticket.objects.all()

    def form_valid(self, form):
        """
        Save user that created the ticket into the model
        """
        user = self.request.user
        form.instance.created_by = user.username
        return super(TicketCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Return Bad Request response if form is invalid
        """
        response = super().form_invalid(form)
        response.status_code = 400
        return response
