from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants_recommendation.restaurants.models import Restaurant, RestaurantLocation
from restaurants_recommendation.restaurants.serializers import (
    LocationListSerializer,
    RestaurantDetailSerializer,
)
from restaurants_recommendation.reviews.serializers import ReviewListSerializer


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


class RestaurantDetailView(APIView):
    # @TODO: Isauthenticated로 변경하기 @SaJH
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="맛집 상세 정보 조회",
        responses={
            status.HTTP_200_OK: RestaurantDetailSerializer,
        },
    )
    def get(self, request: Request, restaurant_id: int) -> Response:
        """
        맛집 상세 정보를 조회합니다.

        Returns:
            restaurant {
            id (int): id
            restaurant_code (str): 맛집 코드
            location_code (str): 위치 코드
            location (dict): 위치 정보 {
                id(int): id,
                do_si(str): 시,도,
                sgg(str): 시,군,구,
                longitude(str) : 경도,
                latitude(str): 위도
                }
            business_name (str): 사업장명
            licensing_at (str): 인허가 일자
            operating_status (str): 영업 상태
            closure_at (str): 폐업 일자
            floor_area (str): 시설 규모
            water_supply_facility_type (str): 상수도 공급 시설 유형
            number_of_male_employees (int): 남성 종사자 수
            year (str): 년도
            multiple_use_facility (str): 다중이용시설
            grade_classification (str): 등급 구분
            total_facility_size (str): 총 시설 규모
            number_of_female_employees (int): 여성 종사자 수
            surrounding_area_description (str): 주변환경
            sanitary_business_type (str): 위생업태명
            total_employees_count (int): 총 종사자 수
            street_address (str): 도로명 주소
            parcel_address (str): 지번 주소
            postal_code (str): 우편번호
            latitude (str): 위도
            longitude (str): 경도
            rating (float): 평점
            }
        review [
            {
                id (int): id
                rating (float): 평점
                content (str): 내용
                created_at (str): 생성 일자
                updated_at (str): 수정 일자
                restaurant (int): 맛집 id
                user (int): 유저 id
            },...
        ]
        """
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        review_set = restaurant.review_set.all().order_by("-created_at")
        context = {
            "restaurant": RestaurantDetailSerializer(restaurant).data,
            "reviews": ReviewListSerializer(review_set, many=True).data,
        }
        return Response(context, status=status.HTTP_200_OK)
