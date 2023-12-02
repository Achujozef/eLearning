from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.db.models import Avg
import razorpay
from django.conf import settings
import time
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Course, VideoCategory
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


@login_required(login_url='login')
def course_details(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)

        course_details = CourseDetails.objects.get(course=course)
        reviews = Review.objects.filter(course=course)
        videos = Video.objects.filter(course=course)
        author = Author.objects.get(id=course.author.id)
        course_in_cart = Cart.objects.filter(user=request.user, course=course).exists()
        course_already_purchased = PurchasedCourses.objects.filter(user=request.user, course=course).exists()
        lessons = Lesson.objects.filter(course=course)
        price_in_float = float(course.price*100)
        client =razorpay.Client(auth=(settings.KEY,settings.SECRET))
        payment=client.order.create({'amount':price_in_float,'currency':'INR','payment_capture':1})

        context = {
            'course': course,
            'course_details': course_details,
            'reviews': reviews,
            'videos': videos,
            'author': author,
            'lessons':lessons,
            'payment':payment,
        }
        context['course_in_cart'] = course_in_cart
        context['course_already_purchased'] = course_already_purchased
        
        return render(request, 'course_details.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})



def course_list(request):
    try:
        all_courses = Course.objects.all().order_by('-id')
        per_page = 12
        paginator = Paginator(all_courses, per_page)
        page = request.GET.get('page')
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)
        context = {
            'courses': courses,
            'categories': Category.objects.all(),
        }
        return render(request, 'course_list.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


def filter_courses(request, category_id):
    try:
        if category_id == 'all':
            courses = Course.objects.all().order_by('-id')
        else:
            courses = Course.objects.filter(category_id=category_id).order_by('-id')
        context = {
            'courses': courses,
            'categories': Category.objects.all(),
        }
        return render(request, 'course_list.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

def search_courses(request):
    try:
        query = request.GET.get('q', '')
        courses = Course.objects.filter(title__icontains=query).order_by('-id')
        context = {
            'courses': courses,
            'categories': Category.objects.all(),
            'query': query,
        }
        return render(request, 'course_list.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


@login_required(login_url='login')
def purchase_course(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        if PurchasedCourses.objects.filter(user=request.user, course=course).exists():
            pass
        else:
            PurchasedCourses.objects.create(user=request.user, course=course)
        return redirect('course:course_details', course_id=course_id)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def add_to_cart(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        if Cart.objects.filter(user=request.user, course=course).exists():
            pass
        else:
            Cart.objects.create(user=request.user, course=course)
        return redirect('course:course_details', course_id=course_id)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def remove_from_cart(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        cart_entry = Cart.objects.filter(user=request.user, course=course).first()
        if cart_entry:
            cart_entry.delete()
        else:
            pass
        return redirect('course:cart')
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def purchase_cart(request):
    try:
        cart_entries = Cart.objects.filter(user=request.user)
        for cart_entry in cart_entries:
            if PurchasedCourses.objects.filter(user=request.user, course=cart_entry.course).exists():
                pass
            else:
                PurchasedCourses.objects.create(user=request.user, course=cart_entry.course)
            cart_entry.delete()

        return redirect('course:cart')
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def cart(request):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.course.price for item in cart_items)
        if cart_items:
            price_in_float = float(total_amount*100)
            client =razorpay.Client(auth=(settings.KEY,settings.SECRET))
            payment=client.order.create({'amount':price_in_float,'currency':'INR','payment_capture':1})
            context = {
                'cart_items': cart_items,
                'total_amount': total_amount,
                'payment':payment
            }
        else:
            context = {
                'cart_items': cart_items,
                'total_amount': total_amount,
            }
        return render(request, 'cart.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def enrolled_courses(request):
    try:
        enrolled_courses = PurchasedCourses.objects.filter(user=request.user)
        context = {
            'enrolled_courses': enrolled_courses,
        }
        return render(request, 'enrolled_courses.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def course_videos(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        videos = Video.objects.filter(course=course).order_by('order')
        progress, created = Progress.objects.get_or_create(user=request.user, course=course)
        remaining= course.total_modules - progress.completed_modules
        completed_videos = CompletedModules.objects.filter(progress=progress, video__in=videos).values_list('video_id', flat=True)
        context = {
            'course': course,
            'videos': videos,
            'progress': progress,
            'remaining':remaining,
            'completed_videos': completed_videos,
        }
        return render(request, 'course_videos.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='login')
def update_progress(request, course_id, video_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        video = get_object_or_404(Video, id=video_id, course=course)
        progress, created = Progress.objects.get_or_create(user=request.user, course=course)
        if video.order <= progress.completed_modules + 1:
            if not CompletedModules.objects.filter(progress=progress, video=video).exists():
                progress.completed_modules += 1
                progress.video = video
                progress.save()
                CompletedModules.objects.create(progress=progress, video=video)
        return redirect('course:course_videos', course_id=course_id)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


def contact_us(request):
    try:
        return render(request, 'contact_us.html')
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
def career_opportunities(request):
    try:
        return render(request, 'career.html')
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


def submit_contact_form(request):
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                return render(request, 'success_page.html', {'name': name, 'email': email})
        else:
            form = ContactForm()
        return render(request, 'contact_form.html', {'form': form})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

def course_videos_two(request, course_id):
    try:
        course = get_object_or_404(Course, pk=course_id)
        video_categories = VideoCategory.objects.all()
        videos_by_category = {}
        for category in video_categories:
            videos_by_category[category] = course.video_set.filter(category=category).order_by('order')
        context = {
            'course': course,
            'video_categories': video_categories,
            'videos_by_category': videos_by_category,
        }
        return render(request, 'course_2_videos.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def add_course(request):
    try:
        if request.method == 'POST':
            course_form = CourseForm(request.POST, request.FILES)
            details_form = CourseDetailsForm(request.POST)
            if course_form.is_valid() and details_form.is_valid():
                course = course_form.save()
                details = details_form.save(commit=False)
                details.course = course
                details.save()
                return redirect('course:course_list') 
        else:
            course_form = CourseForm()
            details_form = CourseDetailsForm()
        return render(request, 'add_course.html', {'course_form': course_form, 'details_form': details_form})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def dashboard(request):
    try:
        courses = Course.objects.filter(author=request.user)
        total_students = UserVideoAccess.objects.filter(course__in=courses).count()
        average_rating = Course.objects.filter(author=request.user).aggregate(avg_rating=Avg('rating'))['avg_rating']
        context = {
            'courses': courses,
            'total_students': total_students,
            'average_rating': average_rating,
        }
        return render(request, 'dashboard.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
    
@login_required(login_url='author_login')
def author_courses(request):
    try:
        courses = Course.objects.filter(author=request.user)
        context = {
            'courses': courses,
        }
        return render(request, 'author_courses.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def add_video(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        if request.method == 'POST':
            form = VideoForm(request.POST)
            if form.is_valid():
                video = form.save(commit=False)
                video.course = course
                video.save()
                return redirect('course:author_courses') 
        else:
            form = VideoForm()
        return render(request, 'add_video.html', {'form': form, 'course': course})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def add_lesson(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.course = course
                lesson.save()
                return redirect('course:author_courses')
        else:
            form = LessonForm()
        return render(request, 'add_lesson.html', {'form': form, 'course': course})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def edit_course(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        coursedetails=get_object_or_404(CourseDetails, course=course)
        if request.method == 'POST':
            course_form = CourseForm(request.POST, request.FILES, instance=course)
            details_form = CourseDetailsForm(request.POST, instance=coursedetails)
            if course_form.is_valid() and details_form.is_valid():
                course_form.save()
                details_form.save()
                return redirect('course:course_list')  
        else:
            course_form = CourseForm(instance=course)
            details_form = CourseDetailsForm(instance=coursedetails)
        return render(request, 'edit_course.html', {'course_form': course_form, 'details_form': details_form})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def list_videos(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        videos = Video.objects.filter(course=course)
        return render(request, 'list_videos.html', {'course': course, 'videos': videos})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required(login_url='author_login')
def delete_video(request, course_id, video_id):
    try:
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        return redirect('course:list_videos_edit', course_id=course_id)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
    
@login_required(login_url='author_login')
def delete_lesson(request, course_id, lesson_id):
    try:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.delete()
        return redirect('course:add_lesson', course_id=course_id)
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


@login_required(login_url='author_login')
def delete_course(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        course_details = CourseDetails.objects.filter(course=course)
        videos = Video.objects.filter(course=course)
        lessons = Lesson.objects.filter(course=course)
        course_details.delete()
        videos.delete()
        lessons.delete()
        course.delete()
        return redirect('course:author_courses')
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
