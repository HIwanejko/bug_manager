from django.urls import path
from .views.ticket_create_view import TicketCreateView
from .views.ticket_list_view import TicketListView
from .views.ticket_detail_view import TicketDetailView
from .views.ticket_update_view import TicketUpdateView
from .views.ticket_delete_view import TicketDeleteView

app_name = 'tickets'
urlpatterns = [
    path('', TicketListView.as_view(), name='tickets-list'),
    path('create/', TicketCreateView.as_view(), name='tickets-create'),
    path('<int:id>/', TicketDetailView.as_view(), name='tickets-detail'),
    path('<int:id>/update/', TicketUpdateView.as_view(), name='tickets-update'),
    path('<int:id>/delete/', TicketDeleteView.as_view(), name='tickets-delete'),
]
