from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from projects.serializers import DonationSerializer
from projects.models import Donation
from .models import User


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
