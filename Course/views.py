from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import ContactForm
import razorpay
from django.conf import settings
import time
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
    price_in_float = float(course.price*100)
    client =razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({'amount':price_in_float,'currency':'INR','payment_capture':1})
    print(payment)
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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def course_list(request):
    # Get all courses
    all_courses = Course.objects.all().order_by('-id')

    # Number of courses to display per page
    per_page = 12

    # Create a Paginator instance
    paginator = Paginator(all_courses, per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page number
        courses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        courses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results
        courses = paginator.page(paginator.num_pages)

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


def update_progress(request, course_id, video_id):
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(Video, id=video_id, course=course)
    progress, created = Progress.objects.get_or_create(user=request.user, course=course)

    # Check if the video is already completed
    if video.order <= progress.completed_modules + 1:
        # Check if the video is not already marked as completed
        if not CompletedModules.objects.filter(progress=progress, video=video).exists():
            progress.completed_modules += 1
            progress.video = video
            progress.save()

            # Record the completion in CompletedModules
            CompletedModules.objects.create(progress=progress, video=video)

    return redirect('course:course_videos', course_id=course_id)


def contact_us(request):
    return render(request, 'contact_us.html')

def submit_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # Form data is valid, you can access it using cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Process the form data as needed (e.g., send emails, save to database)

            # Redirect to a success page
            return render(request, 'success_page.html', {'name': name, 'email': email})
    else:
        # If the form is not submitted, create a new form instance
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Course, VideoCategory

def course_videos_two(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    video_categories = VideoCategory.objects.all()

    # Fetch all videos for the course and categorize them by category
    videos_by_category = {}
    for category in video_categories:
        videos_by_category[category] = course.video_set.filter(category=category).order_by('order')

    context = {
        'course': course,
        'video_categories': video_categories,
        'videos_by_category': videos_by_category,
    }

    return render(request, 'course_2_videos.html', context)
