from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from ..forms import UpdateUserForm


class UpdateProfileView(View):
    template_name = 'update_profile.html'

    def get(self, request):
        """
        GET: return update screen
        """
        if not request.user.is_authenticated:
            return redirect("index")
        form = UpdateUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        POST: validate update request
        """
        if request.user.is_authenticated:
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            else:
                return render(request, self.template_name, {'form': form}, status=400)
        return redirect("index")
