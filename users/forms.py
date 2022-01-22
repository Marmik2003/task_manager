from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0',
        }
    ))


class UserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'bg-slate-100 px-4 py-2 outline-none rounded-md w-full border-0', }))
