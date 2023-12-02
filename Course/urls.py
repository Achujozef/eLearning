# urls.py
from django.urls import path
from .views import *
app_name = 'course'
urlpatterns = [


    path('course/<int:course_id>/', course_details, name='course_details'),
    path('', course_list, name='course_list'),
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
    path('contact/', contact_us, name='contact_us'),
    path('submit_contact_form/', submit_contact_form, name='submit_contact_form'),
    path('add_course/', add_course, name='add_course'),
    path('dashboard/', dashboard, name='instructor_dashboard'),
    path('instructor/courses/', author_courses, name='author_courses'),
    path('add_video/<int:course_id>/', add_video, name='add_video'),
    path('add_lesson/<int:course_id>/', add_lesson, name='add_lesson'),
    path('edit_course/<int:course_id>/', edit_course, name='edit_course'),
    path('list_videos_edit/<int:course_id>/', list_videos, name='list_videos_edit'),
    path('delete_video/<int:course_id>/<int:video_id>/', delete_video, name='delete_video'),
    path('delete_lesson/<int:course_id>/<int:lesson_id>/', delete_lesson, name='delete_lesson'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),
    path('career/', career_opportunities, name='career_opportunities'),
]

