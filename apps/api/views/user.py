from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response

from ..helpers.common import get_auth0_token, create_auth0_user, get_auth0_user, update_auth0_user, delete_auth0_user
from ...user.models import CustomUser
from ..serializers.user import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        connection = 'Username-Password-Authentication'

        try:
            auth0_user = create_auth0_user(email, password, connection)
            data = request.data.copy()
            data['auth0_user_id'] = auth0_user['user_id']
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(auth0_user_id=auth0_user['user_id'])
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            auth0_user = get_auth0_user(instance.auth0_user_id)
            response = super().retrieve(request, *args, **kwargs)
            response.data['auth0_user'] = auth0_user
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        try:
            update_auth0_user(instance.auth0_user_id, request.data)
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            delete_auth0_user(instance.auth0_user_id)
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
