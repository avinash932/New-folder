from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import VideoContent, Category, Topic
import re

def home(request):
    """Home page - No login required"""
    categories = Category.objects.all().order_by('order')[:8]
    
    # Get featured videos (latest published)
    featured_videos = VideoContent.objects.filter(
        status='published'
    ).order_by('-created_at')[:8]
    
    # Get videos by class/category
    class_categories = Category.objects.filter(name__icontains='class').order_by('order')
    
    context = {
        'categories': categories,
        'featured_videos': featured_videos,
        'class_categories': class_categories,
        'total_videos': VideoContent.objects.filter(status='published').count(),
        'page_title': 'Free Education Videos - No Login Required',
    }
    return render(request, 'content/home.html', context)

def video_list(request):
    """List all videos - No login required"""
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    topic_filter = request.GET.get('topic', '')
    
    # Start with published videos
    videos = VideoContent.objects.filter(status='published')
    
    # Apply filters
    if category_filter:
        videos = videos.filter(category__slug=category_filter)
    
    if topic_filter:
        videos = videos.filter(topic__slug=topic_filter)
    
    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(topic__name__icontains=search_query)
        )
    
    # Ensure valid slugs only
    valid_videos = []
    for video in videos:
        if video.slug and video.slug.strip() and ',' not in video.slug:
            valid_videos.append(video)
    
    categories = Category.objects.all()
    topics = Topic.objects.all()
    
    context = {
        'videos': valid_videos,
        'categories': categories,
        'topics': topics,
        'search_query': search_query,
        'selected_category': category_filter,
        'selected_topic': topic_filter,
        'total_videos': len(valid_videos),
        'page_title': 'All Educational Videos',
    }
    return render(request, 'content/video_list.html', context)

def video_detail(request, slug):
    """Video detail page - No login required"""
    # Clean slug
    slug = slug.strip().replace('"', '').replace("'", "").replace(',', '')
    
    # Get video or return 404
    video = get_object_or_404(VideoContent, slug=slug, status='published')
    
    # Extract YouTube ID if available
    youtube_id = None
    if video.video_url and ('youtube.com' in video.video_url or 'youtu.be' in video.video_url):
        patterns = [
            r'(?:youtube\.com\/watch\?v=|\/embed\/|youtu\.be\/)([\w\-]{11})',
            r'(?:youtube\.com\/watch\?.*v=)([\w\-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, video.video_url)
            if match:
                youtube_id = match.group(1)
                break
    
    # Get related videos (same category)
    related_videos = VideoContent.objects.filter(
        status='published',
        category=video.category
    ).exclude(
        id=video.id
    ).order_by('-created_at')[:6]
    
    # If not enough, get any recent videos
    if len(related_videos) < 3:
        additional = VideoContent.objects.filter(
            status='published'
        ).exclude(
            id=video.id
        ).exclude(
            id__in=[v.id for v in related_videos]
        ).order_by('-created_at')[:6-len(related_videos)]
        related_videos = list(related_videos) + list(additional)
    
    context = {
        'video': video,
        'youtube_id': youtube_id,
        'related_videos': related_videos,
        'page_title': video.title,
    }
    return render(request, 'content/video_detail.html', context)

def videos_by_category(request, category_slug):
    """Videos filtered by category"""
    category = get_object_or_404(Category, slug=category_slug)
    
    videos = VideoContent.objects.filter(
        category=category,
        status='published'
    ).order_by('-created_at')
    
    # Ensure valid slugs
    valid_videos = []
    for video in videos:
        if video.slug and video.slug.strip() and ',' not in video.slug:
            valid_videos.append(video)
    
    categories = Category.objects.all()
    topics = Topic.objects.filter(category=category)
    
    context = {
        'videos': valid_videos,
        'category': category,
        'categories': categories,
        'topics': topics,
        'total_videos': len(valid_videos),
        'page_title': f'{category.name} Videos',
    }
    return render(request, 'content/video_list.html', context)

    meta_description = video.description[:160] if video.description else "Watch this educational video for free on EduVideos"
    meta_keywords = f"education, {video.category.name if video.category else ''}, {video.topic.name if video.topic else ''}"
    
    context = {
        # ... existing context ...
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'og_image': video.get_thumbnail_url(),
    }
    return render(request, 'content/video_detail.html', context)


def videos_by_class(request, class_name):
    """Get videos by class (8, 9, 10, 11, 12)"""
    class_name = class_name.lower()
    
    # Map class names to category slugs
    class_map = {
        '8': 'class-8',
        '9': 'class-9', 
        '10': 'class-10',
        '11': 'class-11',
        '12': 'class-12',
    }
    
    category_slug = class_map.get(class_name)
    if not category_slug:
        # Try to find by name
        category = Category.objects.filter(name__icontains=f'Class {class_name}').first()
        if category:
            category_slug = category.slug
    
    if category_slug:
        return videos_by_category(request, category_slug)
    else:
        return video_list(request)




def videos_by_topic(request, topic_slug):
    """Videos filtered by topic"""
    topic = get_object_or_404(Topic, slug=topic_slug)
    
    videos = VideoContent.objects.filter(
        topic=topic,
        status='published'
    ).order_by('-created_at')
    
    valid_videos = []
    for video in videos:
        if video.slug and video.slug.strip() and ',' not in video.slug:
            valid_videos.append(video)
    
    categories = Category.objects.all()
    topics = Topic.objects.filter(category=topic.category)
    
    context = {
        'videos': valid_videos,
        'topic': topic,
        'categories': categories,
        'topics': topics,
        'total_videos': len(valid_videos),
        'page_title': f'{topic.name} Videos',
    }
    return render(request, 'content/video_list.html', context)

def study_materials(request):
    """Study materials page - PDFs, notes, etc."""
    # Get videos that have PDFs
    videos_with_pdfs = VideoContent.objects.filter(
        status='published',
        detailed_content__pdf_file__isnull=False
    ).distinct()
    
    # Get all PDFs
    pdfs = []
    for video in videos_with_pdfs:
        if video.detailed_content and video.detailed_content.pdf_file:
            pdfs.append({
                'title': video.title,
                'pdf_url': video.detailed_content.pdf_file.url,
                'category': video.category.name if video.category else 'General',
                'video_url': video.get_absolute_url(),
                'size': '1-5 MB',  # You can calculate actual size later
            })
    
    # If no PDFs, show sample
    if not pdfs:
        pdfs = [
            {
                'title': 'Mathematics Formula Sheet',
                'category': 'Mathematics',
                'description': 'Important formulas for Class 10-12',
                'sample': True,
            },
            {
                'title': 'Science Experiments Guide',
                'category': 'Science',
                'description': 'Practical experiments with diagrams',
                'sample': True,
            },
            {
                'title': 'English Grammar Rules',
                'category': 'English',
                'description': 'Complete grammar guide with examples',
                'sample': True,
            },
        ]
    
    categories = Category.objects.all()
    
    context = {
        'pdfs': pdfs,
        'categories': categories,
        'total_pdfs': len(pdfs),
        'page_title': 'Free Study Materials - PDF Downloads',
    }
    return render(request, 'content/study_materials.html', context)

def about(request):
    """About us page"""
    stats = {
        'total_videos': VideoContent.objects.filter(status='published').count(),
        'total_categories': Category.objects.count(),
        'launch_date': '2025',
        'mission': 'To provide free quality education to every student',
    }
    
    team = [
        {
            'name': 'Education Experts',
            'role': 'Content Creators',
            'description': 'Experienced teachers and subject matter experts',
            'icon': 'fas fa-chalkboard-teacher',
        },
        {
            'name': 'Technology Team',
            'role': 'Platform Development',
            'description': 'Dedicated to creating the best learning experience',
            'icon': 'fas fa-laptop-code',
        },
        {
            'name': 'Student Community',
            'role': 'Our Inspiration',
            'description': 'Thousands of students who motivate us daily',
            'icon': 'fas fa-users',
        },
    ]
    
    context = {
        'stats': stats,
        'team': team,
        'page_title': 'About EduVideos - Free Education Platform',
    }
    return render(request, 'content/about.html', context)