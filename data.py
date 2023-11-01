import os

import django
from dotenv import load_dotenv

load_dotenv(".env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import asyncio
import json
import math

import aiohttp
from asgiref.sync import sync_to_async
from tqdm.asyncio import tqdm_asyncio

from restaurants_recommendation.restaurants.models import Restaurant, RestaurantLocation

API_KEY = os.environ.get("API_KEY")
API_URL = os.environ.get("API_URL")
API_ENDPOINTS = eval(os.environ.get("API_ENDPOINTS"))


def map_api_data_to_model(data):
    return {
        "location_code": data["SIGUN_CD"],
        "business_name": data["BIZPLC_NM"],
        "licensing_at": data["LICENSG_DE"],
        "operating_status": data["BSN_STATE_NM"],
        "closure_at": data["CLSBIZ_DE"],
        "floor_area": data["LOCPLC_AR"],
        "water_supply_facility_type": data["GRAD_FACLT_DIV_NM"],
        "number_of_male_employees": data["MALE_ENFLPSN_CNT"],
        "year": data["YY"],
        "multiple_use_facility": data["MULTI_USE_BIZESTBL_YN"],
        "grade_classification": data["GRAD_DIV_NM"],
        "total_facility_size": data["TOT_FACLT_SCALE"],
        "number_of_female_employees": data["FEMALE_ENFLPSN_CNT"],
        "surrounding_area_description": data["BSNSITE_CIRCUMFR_DIV_NM"],
        "sanitary_industry_type": data["SANITTN_INDUTYPE_NM"],
        "sanitary_business_type": data["SANITTN_BIZCOND_NM"],
        "total_employees_count": data["TOT_EMPLY_CNT"],
        "street_address": data["REFINE_ROADNM_ADDR"],
        "parcel_address": data["REFINE_LOTNO_ADDR"],
        "postal_code": data["REFINE_ZIP_CD"],
        "latitude": data["REFINE_WGS84_LAT"],
        "longitude": data["REFINE_WGS84_LOGT"],
    }


async def fetch_rastaurant_count(session, url, endpoint):
    async with session.get(url + endpoint, params={"KEY": API_KEY, "Type": "json"}) as response:
        if response.status == 200:
            data = await response.text()
            return json.loads(data)[endpoint][0]["head"][0]["list_total_count"]
        return 0


async def fetch_restaurant_data(session, url, endpoint, page):
    async with session.get(url + endpoint, params={"KEY": API_KEY, "Type": "json", "pIndex": page, "pSize": 1000}) as response:
        if response.status == 200:
            data = await response.text()
            return json.loads(data)[endpoint][1]["row"]
        return None


@sync_to_async
def get_restaurant_location(sgg):
    return RestaurantLocation.objects.filter(sgg=sgg).first()


@sync_to_async
def save_or_update_restaurant(mapped_data, restaurant_code):
    return Restaurant.objects.update_or_create(defaults=mapped_data, restaurant_code=restaurant_code)


async def save_data_to_db(data_list):
    for data in data_list:
        mapped_data = map_api_data_to_model(data)
        if not (mapped_data["business_name"] and mapped_data["street_address"] and mapped_data["latitude"] and mapped_data["longitude"]):
            continue

        restaurantlocation = await get_restaurant_location(data["SIGUN_NM"].strip())
        if restaurantlocation:
            mapped_data["location"] = restaurantlocation

        await save_or_update_restaurant(mapped_data, mapped_data["business_name"] + "_" + mapped_data["street_address"])


async def data_pipeline(url, endpoints):
    async with aiohttp.ClientSession() as session:
        tasks = []
        total_pages = 0
        for endpoint in endpoints:
            count = await fetch_rastaurant_count(session, url, endpoint)
            pages = math.ceil(count / 1000)
            total_pages += pages

            tasks.extend([fetch_restaurant_data(session, url, endpoint, page) for page in range(1, pages + 1)])

        for data in tqdm_asyncio(asyncio.as_completed(tasks), total=len(tasks), desc="Fetching data"):
            data_list = await data
            await save_data_to_db(data_list)


async def main():
    await data_pipeline(API_URL, API_ENDPOINTS)


if __name__ == "__main__":
    asyncio.run(main())
