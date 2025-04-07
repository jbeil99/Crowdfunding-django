from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User

class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = TaggableManager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

 


class ProjectImages(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Image {self.id}"
