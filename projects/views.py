from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import (
    Project,
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
    CommentSerializer,
    RattingSerializer,
    CommentsReportsSerializer,
    ProjectsReportsSerializer,
    DonationSerializer,
    CategorySerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrAdmin


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        # Get total stats
        total_money_raised = Project.get_total_money_raised()
        total_active_projects = Project.objects.filter(is_active=True).count()
        total_featured = Project.objects.filter(is_featured=True).count()

        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
                "statistics": {
                    "total_money_raised": total_money_raised,
                    "total_active_projects": total_active_projects,
                    "total_featured": total_featured,
                },
            }
        )


class ProjectListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        is_featured = request.query_params.get("is_featured")
        category = request.query_params.get("category")
        user_id = request.query_params.get("user_id")
        user = request.user if request.user.is_authenticated else None
        limit = request.query_params.get("limit")
        is_top = request.query_params.get("is_top")
        latest = request.query_params.get("latest")
        search = request.query_params.get("search")
        tags = request.query_params.get("tags")
        projects = Project.filterProjects(
            is_featured=is_featured,
            category=category,
            tags=tags,
            user=user,
            limit=limit,
            is_top=is_top,
            latest=latest,
            search=search,
            user_id=user_id,
        )
        paginator = CustomPagination()
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
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_object(self, pk):
        # if self.request.user.is_staff:
        #     return get_object_or_404(Project, pk=pk)
        return get_object_or_404(Project, pk=pk, is_active=True)

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectStoreSerializer(
            project, data=request.data, context={"request": request}
        )
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


# Comments
class CommentStore(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        comments = Comments.objects.filter(project=project)
        paginator = PageNumberPagination()
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
        serializer = RattingSerializer(
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
        if pk == 0:
            reports = CommentsReports.objects.all()
        else:
            reports = CommentsReports.objects.filter(pk=pk)

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
            return [IsAdminUser()]
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

    def patch(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectStoreSerializer(
            project,
            data=request.data,
            partial=True,
            context={"request": request, "project": project},
        )

        if serializer.is_valid():
            project = serializer.save(is_active=False)
            project_result = ProjectStoreSerializer(project)

            return Response(project_result.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Donation
class DonationStore(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        if pk == 0:
            donations = Donation.objects.all()
        else:
            project = get_object_or_404(Project, pk=pk)
            donations = Donation.objects.filter(project=project)
        paginator = PageNumberPagination()
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


class ProjectFeatured(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectStoreSerializer(
            project,
            data=request.data,
            partial=True,
            context={"request": request, "project": project},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
