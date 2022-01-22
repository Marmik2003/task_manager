from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView
from .forms import UserLoginForm

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
