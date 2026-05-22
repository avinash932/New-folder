from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('videos/', views.video_list, name='video_list'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),
    path('category/<slug:category_slug>/', views.videos_by_category, name='videos_by_category'),
    path('topic/<slug:topic_slug>/', views.videos_by_topic, name='videos_by_topic'),
    path('class/<str:class_name>/', views.videos_by_class, name='videos_by_class'),
    path('study-materials/', views.study_materials, name='study_materials'),
    path('about/', views.about, name='about'),
]