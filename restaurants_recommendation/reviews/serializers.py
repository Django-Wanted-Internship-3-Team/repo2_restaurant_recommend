from rest_framework.serializers import ModelSerializer

from restaurants_recommendation.reviews.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "content",
            "rating",
            "user",
            "restaurant",
            "created_at",
            "updated_at",
        )

    # TODO : validate rating, is int and is 0-5
    # TODO : validate restaurant, is exists
    # TODO : validate user ?
