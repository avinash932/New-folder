from django.core.management.base import BaseCommand
from django.utils.text import slugify
from content.models import Category, Topic, VideoContent, DetailedContent
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add sample educational content to database'
    
    def handle(self, *args, **options):
        self.stdout.write("📚 Adding sample educational content...")
        
        # Create Categories
        categories_data = [
            {'name': 'Class 8', 'icon': 'fas fa-graduation-cap', 'order': 1},
            {'name': 'Class 9', 'icon': 'fas fa-graduation-cap', 'order': 2},
            {'name': 'Class 10', 'icon': 'fas fa-graduation-cap', 'order': 3},
            {'name': 'Class 11', 'icon': 'fas fa-graduation-cap', 'order': 4},
            {'name': 'Class 12', 'icon': 'fas fa-graduation-cap', 'order': 5},
            {'name': 'Mathematics', 'icon': 'fas fa-calculator', 'order': 6},
            {'name': 'Science', 'icon': 'fas fa-flask', 'order': 7},
            {'name': 'Physics', 'icon': 'fas fa-atom', 'order': 8},
            {'name': 'Chemistry', 'icon': 'fas fa-vial', 'order': 9},
            {'name': 'Biology', 'icon': 'fas fa-dna', 'order': 10},
            {'name': 'English', 'icon': 'fas fa-language', 'order': 11},
            {'name': 'Computer Science', 'icon': 'fas fa-laptop-code', 'order': 12},
            {'name': 'JEE Preparation', 'icon': 'fas fa-rocket', 'order': 13},
            {'name': 'NEET Preparation', 'icon': 'fas fa-stethoscope', 'order': 14},
        ]
        
        categories = {}
        for cat_data in categories_data:
            slug = slugify(cat_data['name'])
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f"  ✅ Created category: {cat_data['name']}")
        
        # Create Topics
        topics_data = [
            # Mathematics topics
            {'name': 'Algebra', 'category': categories['Mathematics']},
            {'name': 'Geometry', 'category': categories['Mathematics']},
            {'name': 'Trigonometry', 'category': categories['Mathematics']},
            {'name': 'Calculus', 'category': categories['Mathematics']},
            
            # Science topics
            {'name': 'Light', 'category': categories['Science']},
            {'name': 'Sound', 'category': categories['Science']},
            {'name': 'Electricity', 'category': categories['Science']},
            {'name': 'Magnetism', 'category': categories['Science']},
            
            # Physics topics
            {'name': 'Mechanics', 'category': categories['Physics']},
            {'name': 'Thermodynamics', 'category': categories['Physics']},
            {'name': 'Optics', 'category': categories['Physics']},
            {'name': 'Electromagnetism', 'category': categories['Physics']},
            
            # Chemistry topics
            {'name': 'Organic Chemistry', 'category': categories['Chemistry']},
            {'name': 'Inorganic Chemistry', 'category': categories['Chemistry']},
            {'name': 'Physical Chemistry', 'category': categories['Chemistry']},
            
            # Biology topics
            {'name': 'Cell Biology', 'category': categories['Biology']},
            {'name': 'Genetics', 'category': categories['Biology']},
            {'name': 'Human Physiology', 'category': categories['Biology']},
        ]
        
        topics = {}
        for topic_data in topics_data:
            slug = slugify(topic_data['name'])
            topic, created = Topic.objects.get_or_create(
                slug=slug,
                category=topic_data['category'],
                defaults={'name': topic_data['name'], 'order': 1}
            )
            topics[topic_data['name']] = topic
            if created:
                self.stdout.write(f"  ✅ Created topic: {topic_data['name']}")
        
        # Sample YouTube educational video URLs
        sample_videos = [
            {
                'title': 'Introduction to Algebra for Class 8',
                'description': 'Learn the basics of algebra including variables, constants and simple equations.',
                'category': categories['Class 8'],
                'topic': topics['Algebra'],
                'video_url': 'https://www.youtube.com/watch?v=NybHckSEQBI',
                'duration': '15:30',
            },
            {
                'title': 'Geometry Basics - Lines and Angles',
                'description': 'Understanding different types of lines, angles and their properties.',
                'category': categories['Mathematics'],
                'topic': topics['Geometry'],
                'video_url': 'https://www.youtube.com/watch?v=6g8q5pO6l3I',
                'duration': '18:45',
            },
            {
                'title': 'Trigonometry for Beginners',
                'description': 'Learn sine, cosine, tangent ratios with practical examples.',
                'category': categories['Class 10'],
                'topic': topics['Trigonometry'],
                'video_url': 'https://www.youtube.com/watch?v=PUB0TaZ7bhA',
                'duration': '22:10',
            },
            {
                'title': 'Introduction to Calculus',
                'description': 'Basic concepts of differential and integral calculus for Class 11.',
                'category': categories['Class 11'],
                'topic': topics['Calculus'],
                'video_url': 'https://www.youtube.com/watch?v=WsQQvHm4lSw',
                'duration': '25:20',
            },
            {
                'title': 'Light Reflection and Refraction',
                'description': 'Complete chapter explanation with numerical problems.',
                'category': categories['Science'],
                'topic': topics['Light'],
                'video_url': 'https://www.youtube.com/watch?v=6g8q5pO6l3I',
                'duration': '30:15',
            },
            {
                'title': 'Electricity Class 10 Complete Chapter',
                'description': 'Ohms law, circuits, resistance and practical applications.',
                'category': categories['Class 10'],
                'topic': topics['Electricity'],
                'video_url': 'https://www.youtube.com/watch?v=GAtj228B5g4',
                'duration': '35:40',
            },
            {
                'title': 'Organic Chemistry Basics',
                'description': 'Introduction to hydrocarbons, functional groups and nomenclature.',
                'category': categories['Chemistry'],
                'topic': topics['Organic Chemistry'],
                'video_url': 'https://www.youtube.com/watch?v=B_ketdzJtY8',
                'duration': '28:50',
            },
            {
                'title': 'Cell Structure and Function',
                'description': 'Detailed explanation of cell organelles and their functions.',
                'category': categories['Biology'],
                'topic': topics['Cell Biology'],
                'video_url': 'https://www.youtube.com/watch?v=URUJD5NEXC8',
                'duration': '20:25',
            },
            {
                'title': 'Mechanics - Laws of Motion',
                'description': 'Newtons laws of motion with practical examples and problems.',
                'category': categories['Physics'],
                'topic': topics['Mechanics'],
                'video_url': 'https://www.youtube.com/watch?v=kKKM8Y-u7ds',
                'duration': '32:10',
            },
            {
                'title': 'English Grammar - Tenses',
                'description': 'Complete guide to all English tenses with examples.',
                'category': categories['English'],
                'topic': None,
                'video_url': 'https://www.youtube.com/watch?v=8Gy6BQ4ou-M',
                'duration': '40:00',
            },
        ]
        
        # Create Videos
        for i, video_data in enumerate(sample_videos):
            slug = slugify(video_data['title'])
            video, created = VideoContent.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': video_data['title'],
                    'description': video_data['description'],
                    'category': video_data['category'],
                    'topic': video_data.get('topic'),
                    'video_url': video_data['video_url'],
                    'duration': video_data['duration'],
                    'status': 'published',
                    'content_type': 'youtube',
                    'created_at': timezone.now()
                }
            )
            
            if created:
                # Create detailed content for some videos
                if i % 2 == 0:  # Every second video gets detailed content
                    DetailedContent.objects.create(
                        video=video,
                        content=f"""
                        <h3>Detailed Explanation for {video.title}</h3>
                        <p>This video covers the fundamental concepts in detail.</p>
                        
                        <h4>Key Concepts:</h4>
                        <ul>
                            <li>Basic principles and definitions</li>
                            <li>Step-by-step problem solving</li>
                            <li>Real-world applications</li>
                            <li>Common mistakes to avoid</li>
                        </ul>
                        
                        <h4>Learning Objectives:</h4>
                        <ol>
                            <li>Understand core concepts</li>
                            <li>Solve basic problems</li>
                            <li>Apply knowledge to real situations</li>
                            <li>Prepare for exams</li>
                        </ol>
                        """,
                        important_points="""
                        1. Always remember the basic formulas
                        2. Practice regularly
                        3. Understand the concepts, don't just memorize
                        4. Review previous chapters regularly
                        """,
                        practice_questions="""
                        Q1: What is the main concept explained in this video?
                        Q2: Solve the example problem shown at 10:25
                        Q3: How would you apply this concept in daily life?
                        """,
                        additional_resources="""
                        - Recommended textbook: Chapter 3, Page 45-78
                        - Practice workbook: Exercise 2.1 to 2.5
                        - Online quiz: www.example.com/quiz
                        """
                    )
                
                self.stdout.write(f"  ✅ Created video: {video_data['title'][:40]}...")
        
        self.stdout.write(self.style.SUCCESS(f"""
🎉 Sample data added successfully!

📊 Statistics:
   - Categories: {Category.objects.count()}
   - Topics: {Topic.objects.count()}
   - Videos: {VideoContent.objects.count()}
   - Detailed Content: {DetailedContent.objects.count()}

🌐 Website is now ready with sample content!
   Homepage: http://127.0.0.1:8000/
   Admin: http://127.0.0.1:8000/admin/
   
   Username: admin (or your superuser)
   Password: your password
        """))