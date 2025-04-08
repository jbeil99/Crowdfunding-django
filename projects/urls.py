from django.urls import path
from .views import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    ProjectImageUploadAPIView,
    ImageDetailAPIView,
    CommentStore,
    CommentDetailAPIView,
    RattingDetailAPIView,
    RattingStore,
    CommentsReportsDetailAPIView,
    CommentsReportsStore,
    ProjectReportsStore,
    ProjectReportsDetailAPIView,
    CancelProjectView,
)

urlpatterns = [
    path("projects/", ProjectListCreateAPIView.as_view(), name="project-list-create"),
    path("projects/<int:pk>/", ProjectDetailAPIView.as_view(), name="project-detail"),
    path(
        "projects/<int:pk>/images/",
        ProjectImageUploadAPIView.as_view(),
        name="project-images-upload",
    ),
    path(
        "projects/images/<int:pk>/", ImageDetailAPIView.as_view(), name="image-detail"
    ),
    path("projects/comments/", CommentStore.as_view(), name="project-comments-store"),
    path(
        "projects/comments/<int:pk>",
        CommentDetailAPIView.as_view(),
        name="project-comments-detail",
    ),
    path("projects/ratings", RattingStore.as_view(), name="project-ratings-store"),
    path(
        "projects/ratings/<int:pk>",
        RattingDetailAPIView.as_view(),
        name="project-ratings-detail",
    ),
    path(
        "projects/reports", ProjectReportsStore.as_view(), name="project-reports-store"
    ),
    path(
        "projects/reports/<int:pk>",
        ProjectReportsDetailAPIView.as_view(),
        name="project-reports-detail",
    ),
    path(
        "projects/comments/reports",
        CommentsReportsStore.as_view(),
        name="comments-reports-store",
    ),
    path(
        "projects/comments/reports/<int:pk>",
        CommentsReportsDetailAPIView.as_view(),
        name="comments-reports-detail",
    ),
    path(
        "projects/<int:pk>/cancel/",
        CancelProjectView.as_view(),
        name="project-cancel",
    ),
]
