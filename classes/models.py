from django.db import models

class ClassLevel(models.Model):
    name = models.CharField(max_length=50)  # 8th, 9th, 10th, etc.
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fas fa-school')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

# Link ClassLevel to Category in content app