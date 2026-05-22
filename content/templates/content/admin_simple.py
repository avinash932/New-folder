from django.contrib import admin
from .models import Category, Topic, VideoContent, DetailedContent

# Simple admin registration without custom actions
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(VideoContent)
admin.site.register(DetailedContent)