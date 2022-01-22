from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserSignUpForm

class SignUpView(generic.CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
