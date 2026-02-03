from django.contrib import admin
from django import forms
from django.utils.html import mark_safe

from courses.models import Category, Course


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description', 'active', 'category']
    search_fields = ['subject', 'description']
    list_filter = ['id', 'subject']
    form = CourseForm
    readonly_fields = ['avatar']

    def avatar(self, course):
        return mark_safe(f'<img src="{course.image.url}" width="150" />')


admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
