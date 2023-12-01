from django.db import models
from Userauth.models import *


class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='author_images/', blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.name
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title
    
class Course(models.Model):
    title = models.CharField(max_length=255)
    first_description = models.TextField()
    second_description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    students_enrolled = models.PositiveIntegerField()
    category =models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    total_modules = models.PositiveIntegerField( default=0)

    def __str__(self):
        return self.title

class CourseDetails(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    hours_of_video = models.PositiveIntegerField()
    coding_exercises = models.PositiveIntegerField()
    articles = models.PositiveIntegerField()
    access_on_mobile_and_tv = models.BooleanField(default=True)
    certificate_of_completion = models.BooleanField(default=True)


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    featured_review = models.TextField()
    star = models.PositiveIntegerField()

class VideoCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField() 
    is_free = models.BooleanField(default=False)
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  
    def __str__(self):
        return self.title

class UserVideoAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    has_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Access"


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.course.title})"


class PurchasedCourses(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    # razor_pay_order_id =models.CharField(max_length=100,null=True,blank=True)
    # razor_pay_payment_id =models.CharField(max_length=100,null=True,blank=True)
    # razor_pay_payment_signature =models.CharField(max_length=100,null=True,blank=True)

    
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} (Purchased on {self.purchase_date})"
    
class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.user.username} - {self.course.title} Progress"
    
class Lesson(models.Model):
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.content
    
class CompletedModules(models.Model):
    progress=models.ForeignKey(Progress, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)