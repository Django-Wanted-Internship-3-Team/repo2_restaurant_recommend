import requests
from celery import shared_task

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.users.models import User


@shared_task
def demo():
    return "demo"


def recommend_restaurants(user: User, distance: float = 0.5, count: int = 5):
    """식당 추천 기능"""

    try:
        # TODO : replace to query statement.
        qeuryset = Restaurant.objects.all()
        restaurants = [restaurant for restaurant in qeuryset if restaurant.distance_with(user) <= 0.5]
        restaurants.sort(key=lambda r: r.rating, reverse=True)

        return restaurants[:5]
    except Exception as e:  # float parsing exception.
        return []


def post_webhook(user: User):
    base_url = "http://localhost:8000/api/restaurants"

    data = {
        "username": "LunchHere",
        "content": f"Hello {user.username}, Your LunchHere!",
        "embeds": [
            {
                "author": {
                    "name": f"{restaurant.business_name}",
                    "url": f"{base_url}/{restaurant.id}",
                },
            }
            for restaurant in recommend_restaurants(user)
        ],
    }

    requests.post(user.webhook, json=data)


@shared_task
def recommend_restaurants_to_user():
    users = User.objects.filter(is_lunch_recommend=True)

    for user in users:
        post_webhook(user)
