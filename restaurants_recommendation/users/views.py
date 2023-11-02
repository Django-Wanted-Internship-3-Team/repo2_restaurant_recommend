from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants_recommendation.users.models import User
from restaurants_recommendation.users.serializers import (
    UserDetailSerializer,
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


class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저 상세 정보 조회",
        responses={status.HTTP_200_OK: UserSerializer},
    )
    def get(self, request: Request, user_id: int) -> Response:
        """
        사용자 상세 정보를 조회합니다.

        Returns:
            username (str): 사용자 계정 이름.
            latitude (str): 사용자의 위치 중 위도
            longitude (str): 사용자의 위치 중 경도
            is_lunch_recommend (bool): 점심 메뉴 추천 사용여부
            created_at (str): 사용자 계정 생성 일자
            updated_at (str): 사용자 계정 수정 일자
        """
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="유저 정보 업데이트",
        request_body=UserDetailSerializer,
        responses={status.HTTP_200_OK: UserSerializer},
    )
    def put(self, request: Request, user_id: int) -> Response:
        """
        사용자의 브라우저를 통해 현재 위치의 위도, 경도 값을 받아 유저의 위치를 업데이트하고, 점심 메뉴 추천 True 또는 False 값을 받아 해당 기능의 사용 여부를 결정할 수 있습니다.

        Args:
            user_id (int): 사용자의 고유 식별자
            latitude (str): 사용자의 위치 중 위도
            longitude (str): 사용자의 위치 중 경도
            is_lunch_recommend (bool): 점심 메뉴 추천 사용여부

        Returns:
            User: 위치 정보, 점심 메뉴 추천 정보가 업데이트된 사용자 객체.
        """
        user = get_object_or_404(User, id=user_id)
        serializer = UserDetailSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
