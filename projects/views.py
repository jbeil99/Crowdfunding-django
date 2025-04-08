from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Project, ProjectImages, Comments, Ratting
from .serializers import ProjectStoreSerializer, ProjectDetailSerializer, ImageSerializer, CommentSerializer, RattingSerializer

class ProjectListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request):
        if request.query_params.get('is_featured') == 'true':
            projects =Project.objects.filter(is_featured=True)
        else:
            projects = Project.objects.all()

        serializer = ProjectStoreSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        project_serializer = ProjectStoreSerializer(data=request.data)
        if project_serializer.is_valid():
            project = project_serializer.save()            
            result_serializer = ProjectDetailSerializer(project)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            result_serializer = ProjectDetailSerializer(project)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk): 
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            result_serializer = ProjectDetailSerializer(project)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(project)
        data = serializer.data
        project.delete()
        return Response(data,status=status.HTTP_200_OK)


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
    

class CommentStore(APIView):    
    def post(self, request):
        serialzier = CommentSerializer(data=request.data)
        print(request.data)
        if serialzier.is_valid():
            comment = serialzier.save()
            result_serializer = CommentSerializer(comment)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

    

class CommentDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Comments, pk=pk)
    
    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        comment = self.get_object(pk)
        serializer =CommentSerializer(comment)
        data = serializer.data
        comment.delete()
        return Response(data,status=status.HTTP_200_OK)


class RattingStore(APIView):    
    def post(self, request):
        serialzier = RattingSerializer(data=request.data)
        print(request.data)
        if serialzier.is_valid():
            rate = serialzier.save()
            result_serializer = RattingSerializer(rate)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

    

class RattingDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Ratting, pk=pk)
    
    def get(self, request, pk):
        rate = self.get_object(pk)
        serializer = RattingSerializer(rate)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        rate = self.get_object(pk)
        serializer =RattingSerializer(rate)
        data = serializer.data
        rate.delete()
        return Response(data,status=status.HTTP_200_OK)


class RattingStore(APIView):    
    def post(self, request):
        serialzier = RattingSerializer(data=request.data)
        print(request.data)
        if serialzier.is_valid():
            rate = serialzier.save()
            result_serializer = RattingSerializer(rate)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

    

class RattingDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Ratting, pk=pk)
    
    def get(self, request, pk):
        rate = self.get_object(pk)
        serializer = RattingSerializer(rate)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        rate = self.get_object(pk)
        serializer =RattingSerializer(rate)
        data = serializer.data
        rate.delete()
        return Response(data,status=status.HTTP_200_OK)