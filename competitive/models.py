from django.db import models

class ExamType(models.Model):
    name = models.CharField(max_length=100)  # Engineering, Medical, UPSC, etc.
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='fas fa-trophy')
    
    def __str__(self):
        return self.name

class CompetitiveExam(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # JEE Main, NEET, UPSC CSE, etc.
    slug = models.SlugField(unique=True)
    description = models.TextField()
    official_website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='exam_logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class ExamSubject(models.Model):
    exam = models.ForeignKey(CompetitiveExam, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    
    class Meta:
        unique_together = ['exam', 'slug']
    
    def __str__(self):
        return f"{self.exam.name} - {self.name}"