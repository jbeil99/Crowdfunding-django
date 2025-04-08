from django.urls import path
from .views import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
   ProjectImageUploadAPIView,
    ImageDetailAPIView,
    CommentStore,
    CommentDetailAPIView,
    RattingDetailAPIView,
    RattingStore

)

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:pk>/images/', ProjectImageUploadAPIView.as_view(), name='project-images-upload'),
    path('projects/images/<int:pk>/', ImageDetailAPIView.as_view(), name='image-detail'),
    path('projects/comments/', CommentStore.as_view(), name='project-comments-store'),
    path('projects/comments/<int:pk>', CommentDetailAPIView.as_view(), name='project-comments-detail'),
    path('projects/ratings', RattingStore.as_view(), name='project-ratings-store'),
    path('projects/ratings/<int:pk>', RattingDetailAPIView.as_view(), name='project-ratings-detail'),

]

