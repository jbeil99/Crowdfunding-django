from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from projects.serializers import DonationSerializer
from projects.models import Donation
from .models import User
from .serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 3


class UserDonations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user_donations = Donation.getUserDonations(user)
        paginator = CustomPagination()
        paginated_donations = paginator.paginate_queryset(user_donations, request)
        serializer = DonationSerializer(
            paginated_donations, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        password = request.data.get("current_password")

        if not password:
            return Response(
                {"error": "Current password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()

        return Response(
            {"message": "Your account has been deleted successfully."},
            status=status.HTTP_200_OK,
        )
