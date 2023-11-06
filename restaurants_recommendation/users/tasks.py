from celery import shared_task

from restaurants_recommendation.users.models import User


@shared_task
def demo():
    return "demo"


def recommend_restaurants(user: User):
    pass
