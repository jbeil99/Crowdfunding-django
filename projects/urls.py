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
    DonationStore,
    DonationDetailAPIView,
    CategoryAPIView,
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
    path(
        "projects/<int:pk>/comments",
        CommentStore.as_view(),
        name="project-comments-store",
    ),
    path(
        "comments/<int:pk>",
        CommentDetailAPIView.as_view(),
        name="project-comments-detail",
    ),
    path(
        "projects/<int:pk>/ratings",
        RattingStore.as_view(),
        name="project-ratings-store",
    ),
    path(
        "projects/ratings/<int:pk>",
        RattingDetailAPIView.as_view(),
        name="project-ratings-detail",
    ),
    path(
        "projects/<int:pk>/reports",
        ProjectReportsStore.as_view(),
        name="project-reports-store",
    ),
    path(
        "projects/reports/<int:pk>",
        ProjectReportsDetailAPIView.as_view(),
        name="project-reports-detail",
    ),
    path(
        "comments/reports",
        CommentsReportsStore.as_view(),
        name="comments-reports-store",
    ),
    path(
        "comments/reports/<int:pk>",
        CommentsReportsDetailAPIView.as_view(),
        name="comments-reports-detail",
    ),
    path(
        "projects/<int:pk>/cancel",
        CancelProjectView.as_view(),
        name="project-cancel",
    ),
    path(
        "projects/<int:pk>/donations",
        DonationStore.as_view(),
        name="project-donation-store",
    ),
    path(
        "projects/donation/<int:pk>",
        DonationDetailAPIView.as_view(),
        name="project-donation-detail",
    ),
    path(
        "category",
        CategoryAPIView.as_view(),
        name="category",
    ),
]
