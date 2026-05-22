from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.result_portal, name='result_portal'),
    path('boards/', views.board_results, name='board_results'),
    path('competitive/', views.competitive_results, name='competitive_results'),
    path('redirect/<int:link_id>/', views.redirect_to_result, name='redirect_to_result'),
]