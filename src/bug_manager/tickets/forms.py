from django import forms
from .models import Ticket
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class TicketModelForm(forms.ModelForm):

    created_by = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Ticket
        fields = [
            'name',
            'description',
            'status',
            'created_by',
            'assigned_to'
        ]
        widgets = {'created_by': forms.HiddenInput()}

    def clean_name(self):
        name = self.cleaned_data['name']
        if self._field_is_none_or_empty(name):
            raise ValidationError("Ticket Name is required")
        if not self._field_is_alphanumeric(name.replace(" ", "")):
            raise ValidationError("Your Ticket name must only contain A-z and 0-9 and white space")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if self._field_is_none_or_empty(description):
            raise ValidationError("Ticket Description is required")
        if len(description) > 300:
            raise ValidationError("Ticket Description length must be under 300 characters")
        if not self._field_is_alphanumeric(description.replace(" ", "")):
            raise ValidationError("Your Ticket description must only contain A-z and 0-9 and white space")
        return description

    def clean_assigned_to(self):
        assigned_to = self.cleaned_data['assigned_to']
        if assigned_to == "Unassigned":
            return assigned_to
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            if user.username == assigned_to:
                return assigned_to
        raise ValidationError("User does not exist")

    @staticmethod
    def _field_is_alphanumeric(field) -> bool:
        """
        Verify provided field is alphanumeric
        return Bool: True | False
        """
        return field.isalnum()

    @staticmethod
    def _field_is_none_or_empty(field) -> bool:
        """
        Verify provided field not None or empty
        return Bool: True | False
        """
        return field is None or field == ''
