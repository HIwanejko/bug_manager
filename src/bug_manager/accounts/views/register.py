from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        """
        GET: return register screen
        """
        if request.user.is_authenticated:
            return redirect("index")
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        POST: validate register request
        """
        if not request.user.is_authenticated:
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
            return render(request, self.template_name, {'form': form}, status=401)
