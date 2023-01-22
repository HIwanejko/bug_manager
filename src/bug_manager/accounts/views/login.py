from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        """
        GET: return login screen
        """
        if request.user.is_authenticated:
            return redirect("index")
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        POST: validate accounts request
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        return render(request, self.template_name, {'form': form}, status=401)
