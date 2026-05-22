from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    icon = models.CharField(max_length=50, default='fas fa-folder')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('videos_by_category', kwargs={'category_slug': self.slug})

class Topic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics', null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Choices
CONTENT_TYPE_CHOICES = [
    ('youtube', 'YouTube Video'),
    ('uploaded', 'Uploaded Video'),
    ('vimeo', 'Vimeo Video'),
]

STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
]

class VideoContent(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    
    # Video Details
    video_url = models.URLField(max_length=500, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, default='10:00')
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='youtube')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Video"
        verbose_name_plural = "Videos"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == '':
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            while VideoContent.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        # Clean slug
        self.slug = slugify(self.slug)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'slug': self.slug})
    
    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        # Default educational thumbnails
        defaults = [
            'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=300&q=80',
            'https://images.unsplash.com/photo-1501504905252-473c47e087f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=300&q=80',
            'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=300&q=80',
        ]
        import random
        return random.choice(defaults)
    
    def youtube_id(self):
        import re
        if self.video_url and ('youtube.com' in self.video_url or 'youtu.be' in self.video_url):
            patterns = [
                r'(?:youtube\.com\/watch\?v=|\/embed\/|youtu\.be\/)([\w\-]{11})',
                r'(?:youtube\.com\/watch\?.*v=)([\w\-]{11})',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.video_url)
                if match:
                    return match.group(1)
        return None

class DetailedContent(models.Model):
    video = models.OneToOneField(VideoContent, on_delete=models.CASCADE, related_name='detailed_content')
    content = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    important_points = models.TextField(blank=True)
    practice_questions = models.TextField(blank=True)
    additional_resources = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Detailed Content"
        verbose_name_plural = "Detailed Contents"
    
    def __str__(self):
        return f"Notes for {self.video.title}"