from django.db import models

# Create your models here.


from taggit.managers import TaggableManager






class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    # category 
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = TaggableManager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # creator 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

 
