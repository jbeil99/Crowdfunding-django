from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import (
    Project,
    ProjectImages,
    Comments,
    Ratting,
    Category,
    Donation,
    CommentsReports,
    ProjectsReports,
)
from .serializers import (
    ProjectStoreSerializer,
    ProjectDetailSerializer,
    ImageSerializer,
    CommentSerializer,
    RattingSerializer,
    CommentsReportsSerializer,
    ProjectsReportsSerializer,
    ProjectCancellationSerializer,
    DonationSerializer,
    CategorySerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrAdmin


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 3


# TODO: Change the payload user  to the request user
class ProjectListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        is_featured = request.query_params.get("is_featured")
        category = request.query_params.get("category")
        user = request.query_params.get("user")
        limit = request.query_params.get("limit")
        is_top = request.query_params.get("is_top")
        latest = request.query_params.get("latest")
        search = request.query_params.get("search")
        tags = request.query_params.get("tags")
        projects = Project.filterProjects(
            is_featured=is_featured,
            category=category,
            tags=tags,
            user_id=user,
            limit=limit,
            is_top=is_top,
            latest=latest,
            search=search,
        )

        paginator = PageNumberPagination()
        paginated_Projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectStoreSerializer(
            paginated_Projects, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        project_serializer = ProjectStoreSerializer(
            data=request.data, context={"request": request}
        )
        if project_serializer.is_valid():
            project = project_serializer.save(user=request.user)
            result_serializer = ProjectDetailSerializer(
                project, context={"request": request}
            )
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
        serializer = ProjectDetailSerializer(project, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            result_serializer = ProjectDetailSerializer(
                project, context={"request": request}
            )
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(
            project, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            result_serializer = ProjectDetailSerializer(
                project, context={"request": request}
            )
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(project, context={"request": request})
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
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        comments = Comments.objects.filter(project=project)
        paginator = CustomPagination()
        paginated_comments = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(
            paginated_comments, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        serialzier = CommentSerializer(data=request.data)
        if serialzier.is_valid():
            project = get_object_or_404(Project, pk=pk)
            comment = serialzier.save(user=request.user, project=project)
            result_serializer = CommentSerializer(comment, context={"request": request})
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
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        ratings = Ratting.objects.filter(project=project)
        paginator = PageNumberPagination()
        paginated_ratings = paginator.paginate_queryset(ratings, request)
        serializer = CommentSerializer(
            paginated_ratings, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serialzier = RattingSerializer(data=request.data)
        if serialzier.is_valid():
            rate = serialzier.save(user=request.user, project=project)
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
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        comment = get_object_or_404(Comments, pk=pk)
        reports = CommentsReports.objects.filter(comment=comment)
        paginator = PageNumberPagination()
        paginated_reports = paginator.paginate_queryset(reports, request)
        serializer = CommentsReportsSerializer(
            paginated_reports, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        serialzier = CommentsReportsSerializer(data=request.data)
        if serialzier.is_valid():
            comment = get_object_or_404(Comments, pk=pk)
            report = serialzier.save(user=request.user, comment=comment)
            result_serializer = CommentsReportsSerializer(report)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsReportsDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(CommentsReports, pk=pk)

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
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        reports = ProjectsReports.objects.filter(project=project)
        paginator = PageNumberPagination()
        paginated_reports = paginator.paginate_queryset(reports, request)
        serializer = ProjectsReportsSerializer(
            paginated_reports, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        serialzier = ProjectsReportsSerializer(data=request.data)
        if serialzier.is_valid():
            project = get_object_or_404(Project, pk=pk)
            report = serialzier.save(user=request.user, project=project)
            result_serializer = ProjectsReportsSerializer(report)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectReportsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        return get_object_or_404(ProjectsReports, pk=pk)

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
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def post(self, request, pk):
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


# Donation
class DonationStore(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        donations = Donation.objects.filter(project=project)
        paginator = CustomPagination()
        paginated_donations = paginator.paginate_queryset(donations, request)
        serializer = DonationSerializer(
            paginated_donations, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        serialzier = DonationSerializer(data=request.data)
        if serialzier.is_valid():
            project = get_object_or_404(Project, pk=pk)
            rate = serialzier.save(user=request.user, project=project)
            result_serializer = DonationSerializer(rate)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        return get_object_or_404(Donation, pk=pk)

    def get(self, request, pk):
        rate = self.get_object(pk)
        serializer = DonationSerializer(rate)
        return Response(serializer.data)

    # def delete(self, request, pk):
    #     rate = self.get_object(pk)
    #     serializer = RattingSerializer(rate)
    #     data = serializer.data
    #     rate.delete()
    #     return Response(data, status=status.HTTP_200_OK)


# Cateory
class CategoryAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        serialzier = CategorySerializer(data=request.data)
        if serialzier.is_valid():
            category = serialzier.save()
            result = CategorySerializer(category)
            return Response(result.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: some projects fields ony admin can change it ( may be a differnet serializer)
