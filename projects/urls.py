from django.urls import path
from .views import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
   ProjectImageUploadAPIView,
    ImageListAPIView,
    ImageDetailAPIView
)

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='album-list-create'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='album-detail'),
    path('projects/<int:pk>/images/', ProjectImageUploadAPIView.as_view(), name='album-images-upload'),
    path('projects/images/', ImageListAPIView.as_view(), name='image-list'),
    path('projects/images/<int:pk>/', ImageDetailAPIView.as_view(), name='image-detail'),
]

