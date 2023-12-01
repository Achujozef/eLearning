# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('author/register/', AuthorRegisterView.as_view(), name='author_register'),
    path('author-login/', AuthorLoginView.as_view(), name='author_login'),

]
