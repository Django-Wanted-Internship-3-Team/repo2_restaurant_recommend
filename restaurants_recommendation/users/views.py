from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants_recommendation.users.serializers import (
    UserLoginSerializer,
    UserSerializer,
    UserSignupSerializer,
)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="유저 회원가입",
        request_body=UserSignupSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer},
    )
    def post(self, request: Request) -> Response:
        """
        사용자 이름(username)과 비밀번호(password)를 받아 새로운 사용자 계정을 생성합니다.

        Args:
            username (str): 사용자 계정 이름.
            password (str): 사용자 계정 비밀번호.

        Returns:
            User: 생성된 사용자 객체.
        """
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="유저 로그인",
        request_body=UserLoginSerializer,
        responses={status.HTTP_200_OK: UserLoginSerializer},
    )
    def post(self, request: Request) -> Response:
        """
        사용자 이름(username)과 비밀번호(password)를 받아 유저 계정을 활성화하고 JWT 토큰을 발급합니다.

        Args:
            username (str): 사용자 계정 이름.
            password (str): 사용자 계정 비밀번호.

        Returns:
            token: access token과 refresh token
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
