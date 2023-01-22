from django.urls import path
from .views.login import LoginView
from .views.register import RegisterView
from .views.logout import LogoutView
from .views.update_profile import UpdateProfileView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update_profile/', UpdateProfileView.as_view(), name="update_profile")
]
