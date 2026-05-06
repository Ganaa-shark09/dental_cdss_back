from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers import (
    StaffProfileSerializer,
    StaffProfileCreateSerializer,
    StaffProfileUpdateSerializer,
)
from apps.staff.services import StaffService


class StaffProfileListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        profiles = StaffService.list_staff_profiles()
        serializer = StaffProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StaffProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = StaffService.create_staff_profile(serializer.validated_data, request.user)
        response_serializer = StaffProfileSerializer(profile)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class StaffProfileDetailAPIView(APIView):
    def get(self, request, staff_uuid, *args, **kwargs):
        profile = StaffService.get_staff_profile_by_uuid(staff_uuid)
        serializer = StaffProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, staff_uuid, *args, **kwargs):
        serializer = StaffProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = StaffService.update_staff_profile(
            staff_uuid, serializer.validated_data, request.user
        )
        response_serializer = StaffProfileSerializer(profile)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, staff_uuid, *args, **kwargs):
        serializer = StaffProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        profile = StaffService.update_staff_profile(
            staff_uuid, serializer.validated_data, request.user
        )
        response_serializer = StaffProfileSerializer(profile)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
