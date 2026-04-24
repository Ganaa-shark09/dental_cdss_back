from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, UserCreateSerializer
from apps.users.services import UserService


class UserListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        users = UserService.list_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create_user(serializer.validated_data)
        response_serializer = UserSerializer(user)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
