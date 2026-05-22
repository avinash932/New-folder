from django.urls import path
from . import views

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    
    # Legal Pages
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
]