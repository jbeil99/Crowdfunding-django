from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Project, ProjectImages, Comments, Ratting
from .serializers import (
    ProjectStoreSerializer,
    ProjectDetailSerializer,
    ImageSerializer,
    CommentSerializer,
    RattingSerializer,
    CommentsReportsSerializer,
    ProjectsReportsSerializer,
    ProjectCancellationSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrAdmin


class ProjectListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        if request.query_params.get("is_featured") == "true":
            projects = Project.getfeaturedProjects()
        elif request.query_params.get("category") is not None:
            projects = Project.getProjectsByCategory(
                request.query_params.get("category")
            )
        else:
            projects = Project.objects.all()

        paginator = PageNumberPagination()
        paginated_Projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectStoreSerializer(paginated_Projects, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        project_serializer = ProjectStoreSerializer(data=request.data)
        if project_serializer.is_valid():
            project = project_serializer.save(user=request.user)
            result_serializer = ProjectDetailSerializer(project)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

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
        return Response(data, status=status.HTTP_200_OK)


class ProjectImageUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated(), IsOwnerOrAdmin()]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        images = request.FILES.getlist("images")

        if not images:
            return Response(
                {"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        created_images = []
        for image_file in images:
            img = ProjectImages.objects.create(project=project, image=image_file)
            created_images.append(img)

        serializer = ImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImageDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

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


# Comments
class CommentStore(APIView):
    permission_classes = [IsAuthenticated()]

    def post(self, request):
        request["user"] = request.user.id
        serialzier = CommentSerializer(data=request.data)
        print(request.data)
        if serialzier.is_valid():
            comment = serialzier.save()
            result_serializer = CommentSerializer(comment)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(Comments, pk=pk)

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        data = serializer.data
        comment.delete()
        return Response(data, status=status.HTTP_200_OK)


# Ratting
class RattingStore(APIView):
    permission_classes = [IsAuthenticated()]

    def post(self, request):
        request["user"] = request.user.id
        serialzier = RattingSerializer(data=request.data)
        print(request.data)
        if serialzier.is_valid():
            rate = serialzier.save()
            result_serializer = RattingSerializer(rate)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class RattingDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(Ratting, pk=pk)

    def get(self, request, pk):
        rate = self.get_object(pk)
        serializer = RattingSerializer(rate)
        return Response(serializer.data)

    def delete(self, request, pk):
        rate = self.get_object(pk)
        serializer = RattingSerializer(rate)
        data = serializer.data
        rate.delete()
        return Response(data, status=status.HTTP_200_OK)


# comments Reports
class CommentsReportsStore(APIView):
    permission_classes = [IsAuthenticated()]

    def post(self, request):
        request["user"] = request.user.id
        serialzier = CommentsReportsSerializer(data=request.data)
        if serialzier.is_valid():
            report = serialzier.save()
            result_serializer = CommentsReportsSerializer(report)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsReportsDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(Ratting, pk=pk)

    def get(self, request, pk):
        report = self.get_object(pk)
        serializer = CommentsReportsSerializer(report)
        return Response(serializer.data)

    def delete(self, request, pk):
        report = self.get_object(pk)
        serializer = CommentsReportsSerializer(report)
        data = serializer.data
        report.delete()
        return Response(data, status=status.HTTP_200_OK)


# project Reports
class ProjectReportsStore(APIView):
    permission_classes = [IsAuthenticated()]

    def post(self, request):
        request["user"] = request.user.id
        serialzier = ProjectsReportsSerializer(data=request.data)
        if serialzier.is_valid():
            report = serialzier.save()
            result_serializer = ProjectsReportsSerializer(report)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectReportsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(Ratting, pk=pk)

    def get(self, request, pk):
        report = self.get_object(pk)
        serializer = ProjectsReportsSerializer(report)
        return Response(serializer.data)

    def delete(self, request, pk):
        report = self.get_object(pk)
        serializer = ProjectsReportsSerializer(report)
        data = serializer.data
        report.delete()
        return Response(data, status=status.HTTP_200_OK)


class CancelProjectView(APIView):
    permission_classes = [IsAuthenticated(), IsOwnerOrAdmin()]

    def post(self, request, pk):
        print(request)
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectCancellationSerializer(
            data=request.data, context={"request": request, "project": project}
        )

        if serializer.is_valid():
            project.is_active = False
            project.save()
            return Response(
                {"message": "Project successfully canceled"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
