from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, LoginForm
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