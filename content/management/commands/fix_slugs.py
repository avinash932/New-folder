from django.core.management.base import BaseCommand
from django.utils.text import slugify
from content.models import VideoContent, Category, Topic

class Command(BaseCommand):
    help = 'Fix all empty or invalid slugs'
    
    def handle(self, *args, **options):
        self.stdout.write("🔧 Starting slug fix process...")
        
        # Fix VideoContent slugs
        videos = VideoContent.objects.all()
        video_fixed = 0
        
        for video in videos:
            old_slug = video.slug
            
            if not video.slug or video.slug.strip() == '' or ',' in video.slug:
                base_slug = slugify(video.title)
                slug = base_slug
                counter = 1
                
                while VideoContent.objects.filter(slug=slug).exclude(id=video.id).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                video.slug = slug
                video.save(update_fields=['slug'])
                video_fixed += 1
                
                self.stdout.write(
                    f"  ✅ Video: '{video.title[:30]}...'"
                    f" | Old: '{old_slug}' → New: '{slug}'"
                )
        
        # Fix Category slugs
        category_fixed = 0
        for category in Category.objects.all():
            if not category.slug or category.slug.strip() == '':
                category.slug = slugify(category.name)
                category.save(update_fields=['slug'])
                category_fixed += 1
        
        # Fix Topic slugs
        topic_fixed = 0
        for topic in Topic.objects.all():
            if not topic.slug or topic.slug.strip() == '':
                topic.slug = slugify(topic.name)
                topic.save(update_fields=['slug'])
                topic_fixed += 1
        
        self.stdout.write(self.style.SUCCESS(f"""
🎉 Slug fix completed successfully!

📊 Statistics:
   - Videos fixed: {video_fixed}
   - Categories fixed: {category_fixed}
   - Topics fixed: {topic_fixed}
   - Total objects checked: {videos.count() + Category.objects.count() + Topic.objects.count()}

💡 Next Steps:
   1. Run the server: python manage.py runserver
   2. Check if errors are resolved
   3. Add some sample videos through admin panel
        """))