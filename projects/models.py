from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = TaggableManager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='projects')
    is_featured = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

 


class ProjectImages(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,  related_name='images')
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Image {self.id}"



class Ratting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,  related_name='ratting')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detail = models.TextField(blank=True)
    rate = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=Decimal('0.0'),
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} rate {self.project}'
    


class Comments(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,  related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  related_name='comments')
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} comment on {self.project}'



class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='donations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('1.0'))]
    )

    def __str__(self):
        return f'{self.user} donted to ${self.project}'


class CommentsReports(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reports_comments')
    comment = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports_comments')
    details = models.TextField()
    
    def __str__(self):
        return f'{self.user} reported ${self.comment}'



class ProjectsReports(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reports')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    details = models.TextField()
    
    def __str__(self):
        return f'{self.user} reported ${self.project}'