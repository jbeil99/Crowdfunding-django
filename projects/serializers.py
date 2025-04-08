from rest_framework import serializers
from .models import (
    Project,
    ProjectImages,
    Comments,
    Ratting,
    CommentsReports,
    ProjectsReports,
)
from taggit.serializers import TagListSerializerField, TaggitSerializer
from accounts.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImages
        fields = ["id", "image", "title", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class CommentSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = CommentsReports
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class ProjectsReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsReports
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class ProjectDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)
    ratting = RattingSerializer(many=True, read_only=True)
    user = UserSerializer()

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
            "user",
            "tags",
            "comments",
            "ratting",
        ]
        read_only_fields = ["id", "created_at"]


class ProjectStoreSerializer(TaggitSerializer, serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    tags = TagListSerializerField(required=False)

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
        ]
        read_only_fields = ["id"]

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

            now = datetime.datetime.now()
            if data["start_time"].replace(tzinfo=None) < now:
                raise serializers.ValidationError(
                    {"start_time": "Start time cannot be in the past"}
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


# TODO: Add serializer for admin view to get reports
