from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import VideoContent, Category, Topic

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    
    def items(self):
        return ['home', 'video_list']
    
    def location(self, item):
        return reverse(item)

class VideoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return VideoContent.objects.filter(status='published')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('video_detail', kwargs={'slug': obj.slug})

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    
    def items(self):
        return Category.objects.all()
    
    def location(self, obj):
        return reverse('videos_by_category', kwargs={'category_slug': obj.slug})

class TopicSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        return Topic.objects.all()
    
    def location(self, obj):
        return reverse('videos_by_topic', kwargs={'topic_slug': obj.slug})