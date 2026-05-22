from django.contrib import admin
from .models import ExamType, CompetitiveExam, ExamSubject

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CompetitiveExam)
class CompetitiveExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'slug']
    list_filter = ['exam_type']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam', 'slug']
    list_filter = ['exam']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'exam__name']