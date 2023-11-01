from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants_recommendation.restaurants.models import RestaurantLocation
from restaurants_recommendation.restaurants.serializers import LocationListSerializer


class LocationListView(APIView):
    # @TODO: Isauthenticated로 변경하기 @SaJH
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="시군구 리스트 조회",
        responses={
            status.HTTP_200_OK: LocationListSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        """
        시군구 리스트를 조회합니다.

        Returns:
            id (int): id
            do_si (str): 시,도
            sgg (str): 시,군,구
            longitude (str): 경도
            latitude (str): 위도
        """
        locations = RestaurantLocation.objects.all()
        serializer = LocationListSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
