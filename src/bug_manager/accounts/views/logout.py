from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import logout


class LogoutView(View):
    logout_redirect = 'accounts:login'

    def post(self, request):
        """
        POST: log user out
        """
        if request.user.is_authenticated:
            logout(request)
            return redirect(self.logout_redirect)
        return HttpResponse(status=401)
