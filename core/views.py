
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Homepage view"""
    return render(request, 'core/home.html')

def about(request):
    """About page view"""
    context = {
        'title': 'About EduLearn - Free Education Platform',
        'meta_description': 'Learn about EduLearn - our mission to provide free education for classes 8-12 and competitive exams like JEE, NEET, UPSC, SSC.',
    }
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page view"""
    context = {
        'title': 'Contact Us - EduLearn Support',
        'meta_description': 'Get in touch with EduLearn team for queries, suggestions, or support related to educational content.',
    }
    return render(request, 'core/contact.html', context)

def search(request):
    """Search functionality"""
    query = request.GET.get('q', '')
    context = {
        'query': query,
        'title': f'Search Results for "{query}" - EduLearn',
        'meta_description': f'Search educational content for {query} on EduLearn platform.',
    }
    return render(request, 'core/search.html', context)

def privacy_policy(request):
    """Privacy Policy page"""
    return render(request, 'core/privacy.html')

def terms_of_service(request):
    """Terms of Service page"""
    return render(request, 'core/terms.html')

def disclaimer(request):
    """Disclaimer page"""
    return render(request, 'core/disclaimer.html')