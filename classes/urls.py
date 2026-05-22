from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.class_list, name='class_list'),
    path('<int:class_number>/', views.class_detail, name='class_detail'),
    path('<int:class_number>/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
]