from django.urls import path
from . import views

app_name = 'competitive'

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('<slug:exam_slug>/', views.exam_detail, name='exam_detail'),
    path('<slug:exam_slug>/syllabus/', views.exam_syllabus, name='exam_syllabus'),
    path('<slug:exam_slug>/previous-papers/', views.previous_papers, name='previous_papers'),
]