from django.db import models
from django.urls import reverse


class Ticket(models.Model):

    TICKET_STATUS_CHOICES = (
        ("Open", "Open"),
        ("Closed", "Closed")
    )

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=300)
    status = models.TextField(choices=TICKET_STATUS_CHOICES, default="Opened")
    assigned_to = models.CharField(max_length=30, default="Unassigned")
    opened_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=30)

    def get_absolute_url(self):
        return reverse("tickets:tickets-detail", kwargs={"id": self.id})
