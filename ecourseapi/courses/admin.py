from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.db.models.aggregates import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe
from courses.models import Category, Course, Lesson


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False

    class Meta:
        model = Course
        fields = '__all__'


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description', 'active', 'category']
    search_fields = ['subject', 'description']
    list_filter = ['id', 'subject']
    form = CourseForm
    readonly_fields = ['avatar']

    def avatar(self, course):
        return mark_safe(f'<img src="{course.image.url}" width="150" />')


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm


class MyAdminSite(admin.AdminSite):
    site_header = "eCourse App"

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    def course_stats(self, request):
        stats = Category.objects.annotate(c=Count('course')).values('id', 'name', 'c')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


admin_site = MyAdminSite()
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
