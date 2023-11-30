from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import *


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Retrieve related details
    course_details = CourseDetails.objects.get(course=course)
    reviews = Review.objects.filter(course=course)
    videos = Video.objects.filter(course=course)
    author = Author.objects.get(id=course.author.id)
    course_in_cart = Cart.objects.filter(user=request.user, course=course).exists()
    course_already_purchased = PurchasedCourses.objects.filter(user=request.user, course=course).exists()
    lessons = Lesson.objects.filter(course=course)
    context = {
        'course': course,
        'course_details': course_details,
        'reviews': reviews,
        'videos': videos,
        'author': author,
        'lessons':lessons,
    }
    context['course_in_cart'] = course_in_cart
    context['course_already_purchased'] = course_already_purchased
    return render(request, 'course_details.html', context)

def course_list(request):
    courses = Course.objects.all().order_by('-id')  # Latest courses first

    context = {
        'courses': courses,
        'categories': Category.objects.all(),
    }

    return render(request, 'course_list.html', context)

def filter_courses(request, category_id):
    if category_id == 'all':
        courses = Course.objects.all().order_by('-id')
    else:
        courses = Course.objects.filter(category_id=category_id).order_by('-id')

    context = {
        'courses': courses,
        'categories': Category.objects.all(),
    }

    return render(request, 'course_list.html', context)

def search_courses(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(title__icontains=query).order_by('-id')

    context = {
        'courses': courses,
        'categories': Category.objects.all(),
        'query': query,
    }

    return render(request, 'course_list.html', context)

def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the course is already purchased
    if PurchasedCourses.objects.filter(user=request.user, course=course).exists():
       pass
    else:
        # Create a PurchasedCourses entry
        PurchasedCourses.objects.create(user=request.user, course=course)
       

    return redirect('course:course_details', course_id=course_id)


def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the course is already in the cart
    if Cart.objects.filter(user=request.user, course=course).exists():
        pass
    else:
        # Create a Cart entry
        Cart.objects.create(user=request.user, course=course)
        

    return redirect('course:course_details', course_id=course_id)


def remove_from_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the course is in the cart
    cart_entry = Cart.objects.filter(user=request.user, course=course).first()
    if cart_entry:
        # Remove the course from the cart
        cart_entry.delete()
       
    else:
       pass

    return redirect('course:cart')


def purchase_cart(request):
    cart_entries = Cart.objects.filter(user=request.user)

    for cart_entry in cart_entries:
        # Check if the course is already purchased
        if PurchasedCourses.objects.filter(user=request.user, course=cart_entry.course).exists():
            pass
        else:
            # Create a PurchasedCourses entry
            PurchasedCourses.objects.create(user=request.user, course=cart_entry.course)
           

        # Remove the course from the cart
        cart_entry.delete()

    return redirect('course:cart')



def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.course.price for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart.html', context)

def enrolled_courses(request):
    enrolled_courses = PurchasedCourses.objects.filter(user=request.user)

    context = {
        'enrolled_courses': enrolled_courses,
    }

    return render(request, 'enrolled_courses.html', context)

def course_videos(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = Video.objects.filter(course=course).order_by('order')
    progress, created = Progress.objects.get_or_create(user=request.user, course=course)

    context = {
        'course': course,
        'videos': videos,
        'progress': progress,
    }

    return render(request, 'course_videos.html', context)


def update_progress(request, course_id, video_id):
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(Video, id=video_id, course=course)
    progress, created = Progress.objects.get_or_create(user=request.user, course=course)

    # Check if the video is already completed
    if video.order <= progress.completed_modules + 1:
        progress.completed_modules += 1
        progress.video=video
        progress.save()

    return redirect('course:course_videos', course_id=course_id)