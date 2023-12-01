from django import forms
from .models import *
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'first_description', 'second_description', 'thumbnail', 'rating', 'students_enrolled', 'category', 'price', 'author', 'total_modules']

class CourseDetailsForm(forms.ModelForm):
    class Meta:
        model = CourseDetails
        fields = ['hours_of_video', 'coding_exercises', 'articles', 'access_on_mobile_and_tv', 'certificate_of_completion']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_url', 'is_free', 'category', 'order']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['content']