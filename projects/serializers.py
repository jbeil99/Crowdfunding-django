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
        read_only_fields = ["id", "created_at"]
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
        read_only_fields = ["id", "created_at"]
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
        read_only_fields = ["id", "created_at"]


class ProjectsReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsReports
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user"]


class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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
    donations = DonationSerializer(many=True, read_only=True)
    total_donations = serializers.SerializerMethodField()
    category = CategorySerializer()
    thumbnail = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RattingSerializer(many=True, read_only=True)

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
            "donations",
            "total_donations",
            "category",
            "thumbnail",
            "comments",
            "ratings",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user",
            "donations",
            "user_activities",
        ]

    def get_total_donations(self, obj):
        return obj.get_total_donations()

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return obj.thumbnail.url


class ProjectStoreSerializer(TaggitSerializer, serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    tags = TagListSerializerField(required=False)
    rating = serializers.SerializerMethodField()
    total_donations = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    category = CategorySerializer()

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
            "thumbnail",
        ]
        read_only_fields = ["id", "created_at", "user"]

    def get_rating(slef, obj):
        return obj.get_average_rating()

    def get_total_donations(self, obj):
        return obj.get_total_donations()

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return obj.thumbnail.url

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


class ProjectCancellationSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False)

    def validate(self, data):
        project = self.context.get("project")
        user = self.context.get("request").user
        if project.user != user:
            raise serializers.ValidationError(
                "Only the project owner can cancel a project."
            )

        if not project.canBeCanceld():
            raise serializers.ValidationError(
                "Cannot cancel project that has reached 25% or more of its funding goal."
            )

        return data


# TODO: Add serializer for admin view to get reports
