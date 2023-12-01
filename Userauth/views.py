from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')  
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('course:course_list') 
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('login')  

def Home_view(request):
    print("reached The View")
    return render(request,'home.html')  

class AuthorRegisterView(CreateView):
    template_name = 'author_register.html'
    form_class = AuthorRegistrationForm 
    success_url = reverse_lazy('course:instructor_dashboard')
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.user.is_staff = True
        self.object.user.save()
        login(self.request, self.object.user)  
        return response

class AuthorLoginView(FormView):
    template_name = 'author_login.html'  
    form_class = AuthorLoginForm  
    success_url = reverse_lazy('course:instructor_dashboard') 
    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("Access Denied: Only staff members are allowed to log in.")