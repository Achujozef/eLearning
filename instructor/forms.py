from django import forms
from Course.models import*
from django.forms import inlineformset_factory

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'first_description', 'second_description', 'thumbnail', 'category', 'price', 'total_modules']

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

VideoFormSet = inlineformset_factory(Course, Video, form=VideoForm, extra=1)