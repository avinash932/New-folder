from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<int:test_id>/', views.take_test, name='take_test'),
    path('<int:test_id>/result/', views.test_result, name='test_result'),
]