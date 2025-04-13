from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = TaggableManager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(
        upload_to="images/", default="images/default_thumbnail.jpg"
    )

    def __str__(self):
        return self.title

    @classmethod
    def getAvtiveProjects(cls):
        return cls.objects.filter(is_active=True)

    @classmethod
    def getAcceptedProjects(cls):
        return cls.getAvtiveProjects().filter(is_accepted=True)

    @classmethod
    def getNotAcceptedProjects(cls):
        return cls.getAvtiveProjects().filter(is_accepted=False)

    @classmethod
    def getfeaturedProjects(cls):
        return cls.getAvtiveProjects().filter(is_featured=True)

    @classmethod
    def getProjectsByCategory(cls, category):
        return cls.getAvtiveProjects().filter(category=category)

    @classmethod
    def getProjectsByTags(cls, tag_names):
        return cls.objects.filter(tags__name__in=tag_names)

    @classmethod
    def getUserProjects(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def getTopRatedProjects(cls, limit=5):
        return (
            cls.getAvtiveProjects()
            .annotate(avg_rating=models.Avg("ratings__rate"))
            .order_by("-avg_rating")[:limit]
        )

    @classmethod
    def filterProjects(
        cls,
        is_featured=None,
        category=None,
        tags=None,
        user=None,
        user_id=None,
        limit=None,
        is_top=None,
        latest=None,
        search=None,
    ):
        if user and user.is_staff:
            projects = cls.objects.all()
        else:
            if user_id:
                projects = cls.getUserProjects(user_id)
            else:
                projects = cls.getAcceptedProjects()

        if is_featured == "true":
            projects = projects.filter(is_featured=True)
        if category:
            try:
                if category:
                    category_id = int(category)
                    projects = projects.filter(category=category_id)
            except (ValueError, TypeError):
                projects = projects.filter(category=-1)

        if tags:
            projects = projects.filter(tags__name__in=tags.split(","))

        if search:
            projects = projects.filter(
                models.Q(title__icontains=search) | models.Q(details__icontains=search)
            )

        if latest == "true":
            if limit:
                try:
                    limit = int(limit)
                    projects = projects.order_by("-created_at")[:limit]
                except (ValueError, TypeError):
                    pass
            else:
                projects = projects.order_by("-created_at")[:5]

        if limit:
            try:
                limit = int(limit)
                projects = projects[:limit]
            except (ValueError, TypeError):
                pass

        if is_top == "true":
            return cls.getTopRatedProjects()

        return projects

    def canBeCanceld(self):
        if not self.get_total_donations() or not self.total_target:
            return True
        return self.get_total_donations() / self.total_target * 100 < 25

    def get_average_rating(self):
        average = self.ratings.aggregate(avg_ratings=models.Avg("rate"))["avg_ratings"]
        if average is not None:
            return round(average, 1)
        return 0.0

    def get_total_donations(self):
        return self.donations.aggregate(total=models.Sum("amount"))["total"]

    def get_raters_count(self):
        return self.ratings.count()

    def get_donors_count(self):
        return self.donations.values("user").distinct().count()


class ProjectImages(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"


class Ratting(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    detail = models.TextField(blank=True)
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal("0.0"),
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("5.0")),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} rate {self.project}"


class Comments(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} comment on {self.project}"

    class Meta:
        ordering = ["-created_at"]


class Donation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="donations", null=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="donations"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("1.0"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} donted to ${self.project}"

    @classmethod
    def getUserDonations(cls, user):
        return cls.objects.filter(user=user)


class CommentsReports(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="reports_comments", null=True
    )
    comment = models.ForeignKey(
        Comments, on_delete=models.CASCADE, related_name="reports_comments"
    )
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} reported ${self.comment}"


class ProjectsReports(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="reports", null=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="reports"
    )
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} reported ${self.project}"
