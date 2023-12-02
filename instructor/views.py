# from audioop import avg
# from django.shortcuts import render
# from flask import redirect
# from Course.models import *
# from django.db.models import Avg
# from .forms import *

# def dashboard(request):
#     courses = Course.objects.filter(author=request.user)
#     total_students = UserVideoAccess.objects.filter(course__in=courses).count()
#     average_rating = Course.objects.filter(author=request.user).aggregate(avg_rating=Avg('rating'))['avg_rating']
#     context = {
#         'courses': courses,
#         'total_students': total_students,
#         'average_rating': average_rating,
#     }

#     return render(request, 'dashboard.html', context)

# def author_courses(request):
#     # Assuming request.user is the author
#     courses = Course.objects.filter(author=request.user)

#     context = {
#         'courses': courses,
#     }

#     return render(request, 'author_courses.html', context)


# def add_course(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         first_description = request.POST.get('first_description')
#         second_description = request.POST.get('second_description')
#         thumbnail = request.FILES.get('thumbnail')
#         category_id = request.POST.get('category')
#         price = request.POST.get('price')
#         total_modules = request.POST.get('total_modules')
#         hours_of_video = request.POST.get('hours_of_video')
#         coding_exercises = request.POST.get('coding_exercises')
#         articles = request.POST.get('articles')
#         access_on_mobile_and_tv = request.POST.get('access_on_mobile_and_tv')
#         certificate_of_completion = request.POST.get('certificate_of_completion')
#         access_on_mobile_and_tv = access_on_mobile_and_tv == 'on'
#         certificate_of_completion = certificate_of_completion == 'on'

#         category = Category.objects.get(id=category_id)

#         new_course = Course(
#             title=title,
#             first_description=first_description,
#             second_description=second_description,
#             thumbnail=thumbnail,
#             category=category,
#             price=price,
#             author=request.user,
#             total_modules=total_modules,
#         )
#         new_course.save()

#         course_details = CourseDetails(
#             course=new_course,
#             hours_of_video=hours_of_video,
#             coding_exercises=coding_exercises,
#             articles=articles,
#             access_on_mobile_and_tv=access_on_mobile_and_tv,
#             certificate_of_completion=certificate_of_completion,
#         )
#         course_details.save()

#         return redirect('dashboard')  
#     else:
#         categories = Category.objects.all()
#         return render(request, 'add_course.html', {'categories': categories})

