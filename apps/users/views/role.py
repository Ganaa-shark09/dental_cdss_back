from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import RoleSerializer
from apps.users.services import UserService


class RoleListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        roles = UserService.list_roles()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
