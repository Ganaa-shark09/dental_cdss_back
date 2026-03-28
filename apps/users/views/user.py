from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer


class MeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)