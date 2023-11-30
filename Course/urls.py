# urls.py
from django.urls import path
from .views import *
app_name = 'course'
urlpatterns = [
    path('course/<int:course_id>/', course_details, name='course_details'),
    path('courses/', course_list, name='course_list'),
    path('courses/category/<str:category_id>/', filter_courses, name='filter_courses'),
    path('courses/search/', search_courses, name='search_courses'),
    path('purchase/<int:course_id>/', purchase_course, name='purchase_course'),
    path('add-to-cart/<int:course_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:course_id>/', remove_from_cart, name='remove_from_cart'),
    path('purchase_cart/', purchase_cart, name='purchase_cart'),
    path('cart/', cart, name='cart'),
    path('enrolled-courses/', enrolled_courses, name='enrolled_courses'),
    path('<int:course_id>/videos/', course_videos, name='course_videos'),
    path('<int:course_id>/update_progress/<int:video_id>/', update_progress, name='update_progress'),

]
