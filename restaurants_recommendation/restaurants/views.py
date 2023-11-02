from typing import Any, List, Tuple

from django.db.models import QuerySet
from django.db.models.query_utils import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants_recommendation.common.exceptions import InvalidParameterException
from restaurants_recommendation.common.utils import lat_lon_to_km
from restaurants_recommendation.restaurants.models import Restaurant, RestaurantLocation
from restaurants_recommendation.restaurants.serializers import (
    LocationListSerializer,
    RestaurantDetailSerializer,
    RestaurantListSerializer,
    RestaurantQuerySerializer,
)
from restaurants_recommendation.reviews.serializers import ReviewListSerializer


class LocationListView(APIView):
    permission_classes = [IsAuthenticated]

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


class RestaurantListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=RestaurantQuerySerializer,
        operation_summary="맛집 리스트 조회",
        responses={
            status.HTTP_200_OK: RestaurantListSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        """
        맛집 리스트를 조회합니다.

        Args:
            type (str): 필터 타입
            lat (str): 위도
            lon (str): 경도
            range (float): 반경
            order_by (str): 정렬 기준
            search (str): 검색어
            limit (int): 조회 개수
            offset (int): 조회 시작 위치

        Returns:
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
            operating_status (str): 영업 상태
            closure_at (str): 폐업 일자
            street_address (str): 도로명 주소
            parcel_address (str): 지번 주소
            postal_code (str): 우편번호
            latitude (str): 위도
            longitude (str): 경도
            rating (float): 평점
            distance (str): 거리
        """
        query_serializer = RestaurantQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data
        restaurant_list, restaurant_list_count, restaurant_list_total_count = self.get_restaurants_by_location(**validated_data)
        context = {
            "count": restaurant_list_count,
            "total_count": restaurant_list_total_count,
            "results": RestaurantListSerializer(restaurant_list, many=True).data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def get_restaurants_by_location(
        self, type: str, lat: str, lon: str, range: float, order_by: str, search: str, limit: int, offset: int
    ) -> Tuple[List[Any], int, int]:
        """
        filter_type:
            my_location: 유저의 위경도를 기준으로 반경 내의 맛집을 조회 후 쿼리셋으로 반환
            hold_location: 시군구의 위경도를 기준으로 반경 내의 맛집을 조회 후 쿼리셋으로 반환

        order_by:
            distance: 거리 순으로 정렬
            rating: 평점 순으로 정렬
        """
        q = Q()

        if search:
            q = q & Q(business_name__iexact=search) | Q(restaurant_code__iexact=search)

        restaurants = self.get_filter_type_query(filter_type=type, lat=lat, lon=lon, q=q)
        restaurant_list = []
        point_1 = [lat, lon]

        for restaurant in restaurants:
            point_2 = [restaurant.latitude, restaurant.longitude]
            distance = lat_lon_to_km(point_1=point_1, point_2=point_2)

            if distance <= range:
                restaurant.distance = round(distance, 2)
                restaurant_list.append(restaurant)

        restaurant_list = self.get_ordered_restaurants(restaurant_list, order_by)
        return restaurant_list[offset : offset + limit], len(restaurant_list[offset : offset + limit]), len(restaurant_list)

    def get_filter_type_query(self, filter_type: str, lat: str, lon: str, q: Q) -> QuerySet[Restaurant]:
        if filter_type == "my_location":
            return Restaurant.objects.all().filter(q)
        elif filter_type == "hold_location":
            return Restaurant.objects.filter(
                location__latitude=lat,
                location__longitude=lon,
            ).filter(q)
        else:
            raise InvalidParameterException("Invalid filter type")

    def get_ordered_restaurants(self, restaurant_list, order_by: str) -> List[Any]:
        if order_by == "distance":
            return sorted(restaurant_list, key=lambda x: x.distance)
        elif order_by == "rating":
            return sorted(restaurant_list, key=lambda x: x.rating, reverse=True)
        return restaurant_list


class RestaurantDetailView(APIView):
    permission_classes = [IsAuthenticated]

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
