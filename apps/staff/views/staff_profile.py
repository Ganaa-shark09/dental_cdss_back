from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers import StaffProfileSerializer, StaffProfileCreateSerializer
from apps.staff.services import StaffService


class StaffProfileListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        profiles = StaffService.list_staff_profiles()
        serializer = StaffProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StaffProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = StaffService.create_staff_profile(serializer.validated_data)
        response_serializer = StaffProfileSerializer(profile)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
