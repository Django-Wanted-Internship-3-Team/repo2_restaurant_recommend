from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants_recommendation.reviews.serializers import ReviewSerializer


class ReviewAPIView(APIView):
    """
    Review api view
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="add review into restaurant.",
        request_body=ReviewSerializer,
        responses={
            status.HTTP_201_CREATED: ReviewSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response("badrequest with parameter errors"),
            status.HTTP_401_UNAUTHORIZED: openapi.Response("unauthorized"),
        },
    )
    def post(self, request: Request):
        """
        식당에 리뷰를 등록하는 api
        """
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
