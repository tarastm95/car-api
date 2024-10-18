from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from core.dataclasses.user_dataclass import User
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoverToken

from apps.auth.serializers import EmailSerializer, PasswordSerializer
from apps.users.serializers import UserSerializer
from rest_framework import serializers


# Створюємо ErrorSerializer з унікальним ref_name
class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

    class Meta:
        ref_name = "AuthErrorSerializer"  # Унікальне ім'я для Swagger


UserModel: User = get_user_model()


class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        pass

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer, status.HTTP_400_BAD_REQUEST: ErrorSerializer})
    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecoveryPasswordRequestView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery_password(user)
        return Response(status=status.HTTP_200_OK)


class RecoveryPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user = JWTService.verify_token(token, RecoverToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({"detail": "Your password has been reset."}, status=status.HTTP_200_OK)
