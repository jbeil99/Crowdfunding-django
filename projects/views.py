from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Project, ProjectImages
from .serializers import ProjectWithImagesSerializer, ProjectSerializer, ImageSerializer

class ProjectListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request):
        if request.query_params.get('is_featured') == 'true':
            projects =Project.objects.filter(is_featured=True)
        else:
            projects = Project.objects.all()

        serializer = ProjectSerializer(projects, many=True)
        print(request.query_params)
        return Response(serializer.data)
    
    def post(self, request):
        project_serializer = ProjectWithImagesSerializer(data=request.data)
        if project_serializer.is_valid():
            project = project_serializer.save()            
            result_serializer = ProjectSerializer(project)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectWithImagesSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            result_serializer = ProjectSerializer(project)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk): 
        project = self.get_object(pk)
        serializer = ProjectWithImagesSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            result_serializer = ProjectSerializer(project)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectImageUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        images = request.FILES.getlist('images')
        
        if not images:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        created_images = []
        for image_file in images:
            img = ProjectImages.objects.create(project=project, image=image_file)
            created_images.append(img)
        
        serializer = ImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImageListAPIView(APIView):
    def get(self, request):
        images = ProjectImages.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class ImageDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ProjectImages, pk=pk)
    
    def get(self, request, pk):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)