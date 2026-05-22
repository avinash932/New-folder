from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Topic, VideoContent, DetailedContent

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order', 'get_video_count')
    list_editable = ('order', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    
    def get_video_count(self, obj):
        return obj.videos.count()
    get_video_count.short_description = 'Videos'
    get_video_count.admin_order_field = 'videos__count'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_category', 'slug', 'order', 'get_video_count')
    list_filter = ('category',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('category__name', 'order', 'name')
    
    def get_category(self, obj):
        return obj.category.name if obj.category else "-"
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'
    
    def get_video_count(self, obj):
        return obj.videos.count()
    get_video_count.short_description = 'Videos'

class DetailedContentInline(admin.StackedInline):
    model = DetailedContent
    extra = 0
    fields = ('content', 'important_points', 'practice_questions', 'additional_resources', 'pdf_file')
    verbose_name = "Study Material"
    verbose_name_plural = "Study Materials"

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    # Remove actions attribute if it exists or define it properly
    # actions = None  # या फिर सही actions define करें
    
    list_display = ('title_preview', 'category_display', 'status_badge', 'created_date', 'admin_actions')
    list_filter = ('status', 'content_type', 'category', 'created_at')
    search_fields = ('title', 'description', 'slug')
    readonly_fields = ('created_at', 'updated_at', 'slug_preview', 'video_preview')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'slug_preview', 'description')
        }),
        ('Categorization', {
            'fields': ('category', 'topic')
        }),
        ('Video Details', {
            'fields': ('video_url', 'thumbnail', 'video_preview', 'duration', 'content_type', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [DetailedContentInline]
    ordering = ('-created_at',)
    
    # Custom display methods
    def title_preview(self, obj):
        return format_html('<strong>{}</strong>', obj.title[:50] + ('...' if len(obj.title) > 50 else ''))
    title_preview.short_description = 'Title'
    
    def category_display(self, obj):
        if obj.category:
            return format_html(
                '<span class="badge" style="background: #4e54c8; color: white; padding: 4px 8px; border-radius: 4px;">{}</span>',
                obj.category.name
            )
        return '-'
    category_display.short_description = 'Category'
    
    def status_badge(self, obj):
        colors = {
            'published': 'success',
            'draft': 'warning',
            'archived': 'secondary'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def created_date(self, obj):
        return obj.created_at.strftime('%d %b %Y')
    created_date.short_description = 'Created'
    created_date.admin_order_field = 'created_at'
    
    def admin_actions(self, obj):
        if obj.slug:
            return format_html(
                '<a href="{}" target="_blank" class="button" style="background: #4e54c8; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">View</a>',
                obj.get_absolute_url()
            )
        return '-'
    admin_actions.short_description = 'Actions'
    
    def slug_preview(self, obj):
        if obj.slug:
            return format_html(
                '<code style="background: #f8f9fa; padding: 5px; border-radius: 3px;">{}</code><br>'
                '<small>URL: /video/{}/</small>',
                obj.slug, obj.slug
            )
        return 'Will be auto-generated when saved'
    slug_preview.short_description = 'Slug Preview'
    
    def video_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 200px; border-radius: 5px;" alt="Thumbnail">',
                obj.thumbnail.url
            )
        elif obj.video_url and 'youtube.com' in obj.video_url:
            youtube_id = None
            import re
            match = re.search(r'(?:youtube\.com\/watch\?v=|\/embed\/|youtu\.be\/)([\w\-]{11})', obj.video_url)
            if match:
                youtube_id = match.group(1)
                return format_html(
                    '<img src="https://img.youtube.com/vi/{}/hqdefault.jpg" '
                    'style="max-height: 150px; max-width: 200px; border-radius: 5px;" alt="YouTube Thumbnail">',
                    youtube_id
                )
        return 'No thumbnail available'
    video_preview.short_description = 'Thumbnail Preview'
    
    # Save method to auto-generate slug
    def save_model(self, request, obj, form, change):
        if not obj.slug or obj.slug.strip() == '':
            from django.utils.text import slugify
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)
    
    # Remove or define get_actions method if needed
    def get_actions(self, request):
        actions = super().get_actions(request)
        # You can customize actions here if needed
        return actions

@admin.register(DetailedContent)
class DetailedContentAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'has_pdf', 'created_date', 'updated_date')
    search_fields = ('video__title', 'content', 'important_points')
    list_filter = ('created_at', 'video__category')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Video Link', {
            'fields': ('video',)
        }),
        ('Study Materials', {
            'fields': ('content', 'important_points', 'practice_questions', 'additional_resources')
        }),
        ('PDF File', {
            'fields': ('pdf_file',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def video_title(self, obj):
        return obj.video.title
    video_title.short_description = 'Video Title'
    video_title.admin_order_field = 'video__title'
    
    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF Available'
    
    def created_date(self, obj):
        return obj.created_at.strftime('%d %b %Y')
    created_date.short_description = 'Created'
    created_date.admin_order_field = 'created_at'
    
    def updated_date(self, obj):
        return obj.updated_at.strftime('%d %b %Y')
    updated_date.short_description = 'Updated'
    updated_date.admin_order_field = 'updated_at'