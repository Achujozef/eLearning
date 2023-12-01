from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
class RegistrationForm(UserCreationForm):


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class AuthorRegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'bio']

class AuthorLoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'password']