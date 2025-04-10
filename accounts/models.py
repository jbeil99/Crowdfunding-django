from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    mobile_phone = models.CharField("mobile phone", max_length=15, blank=False)
    profile_picture = models.ImageField(
        upload_to="media/profile_pics",
        null=True,
        blank=True,
        default="images/default_avatar.jpg",
    )
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "mobile_phone"]


class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).total_seconds() < 24 * 60 * 60
