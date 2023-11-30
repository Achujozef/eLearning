from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(UserVideoAccess)
admin.site.register(Video)
admin.site.register(VideoCategory)
admin.site.register(Review)
admin.site.register(CourseDetails)
admin.site.register(Course)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(PurchasedCourses)
admin.site.register(Progress)
admin.site.register(Lesson)