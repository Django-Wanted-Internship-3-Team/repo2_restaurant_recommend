from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from restaurants_recommendation.reviews.serializers import ReviewSerializer


class ReviewAPIView(APIView):
    """
    Review api view
    """

    @swagger_auto_schema(
        operation_summary="add review into restaurant.",
        request_body=ReviewSerializer,
        responses={
            status.HTTP_201_CREATED: ReviewSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response("badrequest with parameter errors"),
            status.HTTP_401_UNAUTHORIZED: openapi.Response("unauthorized"),
        },
    )
    def post(self, request):
        """
        식당에 리뷰를 등록하는 api
        """
