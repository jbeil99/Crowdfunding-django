from rest_framework import serializers
from .models import (
    Project,
    ProjectImages,
    Comments,
    Ratting,
    CommentsReports,
    ProjectsReports,
    Donation,
    Category,
)
from taggit.serializers import TagListSerializerField, TaggitSerializer
from accounts.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImages
        fields = ["id", "image_url", "title", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"
        read_only_fields = ["id", "created_at", "project"]
        extra_kwargs = {"body": {"required": True}}

    def validate_body(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError("Commnet Cant be empty")
        return value


class RattingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ratting
        fields = "__all__"
        read_only_fields = ["id", "created_at", "project"]
        extra_kwargs = {"rate": {"required": True}}

    def validate_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("rate Cant less than zero")
        if value > 5:
            raise serializers.ValidationError("rate Cant more than 5.0")
        return value


class CommentsReportsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommentsReports
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user", "comment"]


class ProjectsReportsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectsReports
        fields = "__all__"
        read_only_fields = ["id", "created_at", "project"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long"
            )
        if len(value) > 250:
            raise serializers.ValidationError(
                "Title must be at most 250 characters long"
            )
        return value

    def validate_description(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                "Details must be at least 20 characters long"
            )
        if len(value) > 2500:
            raise serializers.ValidationError(
                "Title must be at most 2500 characters long"
            )
        return value


class ProjectDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    owner = UserSerializer(source="user")
    total_donations = serializers.SerializerMethodField()
    category = CategorySerializer()
    thumbnail = serializers.SerializerMethodField()
    backers_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "details",
            "created_at",
            "images",
            "total_target",
            "start_time",
            "end_time",
            "owner",
            "tags",
            "is_featured",
            "total_donations",
            "category",
            "thumbnail",
            "backers_count",
            "review_count",
            "is_active",
            "is_accepted",
            "rating",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user",
            "is_accepted",
        ]

    def get_total_donations(self, obj):
        return obj.get_total_donations()

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return obj.thumbnail.url

    def get_backers_count(self, obj):
        return obj.get_donors_count()

    def get_review_count(self, obj):
        return obj.get_raters_count()

    def get_rating(slef, obj):
        return obj.get_average_rating()


class ProjectStoreSerializer(TaggitSerializer, serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    tags = TagListSerializerField(required=True)
    rating = serializers.SerializerMethodField()
    total_donations = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.ImageField(write_only=True, required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_detail = CategorySerializer(source="category", read_only=True)
    backers_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "details",
            "images",
            "total_target",
            "start_time",
            "end_time",
            "user",
            "tags",
            "is_featured",
            "rating",
            "total_donations",
            "category",
            "thumbnail_url",
            "thumbnail",
            "is_active",
            "created_at",
            "category_detail",
            "backers_count",
            "review_count",
            "is_accepted",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user",
            "is_active",
            "is_accepted",
            "created_at",
        ]

    def get_rating(slef, obj):
        return obj.get_average_rating()

    def get_total_donations(self, obj):
        return obj.get_total_donations()

    def get_thumbnail_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return obj.thumbnail.url

    def get_backers_count(self, obj):
        return obj.get_donors_count()

    def get_review_count(self, obj):
        return obj.get_raters_count()

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long"
            )
        if len(value) > 250:
            raise serializers.ValidationError(
                "Title must be at most 250 characters long"
            )
        return value

    def validate_details(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                "Details must be at least 20 characters long"
            )
        if len(value) > 2500:
            raise serializers.ValidationError(
                "Title must be at most 2500 characters long"
            )
        return value

    def validate_total_target(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total target must be greater than zero")
        return value

    def validate(self, data):
        if "start_time" in data and "end_time" in data:
            if data["start_time"] >= data["end_time"]:
                raise serializers.ValidationError(
                    {"end_time": "End time must be after start time"}
                )

            import datetime

            today = datetime.datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            if data["start_time"].replace(tzinfo=None) < today:
                raise serializers.ValidationError(
                    {"start_time": "Start date cannot be in the past"}
                )

        return data

    def create(self, validated_data):
        images_data = validated_data.pop("images", None)
        tags_data = validated_data.pop("tags", [])
        project = Project.objects.create(**validated_data)

        if tags_data:
            project.tags.set(tags_data)

        if images_data:
            for image_data in images_data:
                ProjectImages.objects.create(project=project, image=image_data)

        return project

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", None)
        tags_data = validated_data.pop("tags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        if (
            images_data is not None and images_data
        ):  # Only modify images if data was provided
            instance.images.all().delete()

            for image_data in images_data:
                ProjectImages.objects.create(project=instance, image=image_data)

        return instance


class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectStoreSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ["amount", "project", "user", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Donation amount can't be less than or equal to 0"
            )
        return value
