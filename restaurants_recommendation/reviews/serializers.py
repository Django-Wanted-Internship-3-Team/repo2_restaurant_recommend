from rest_framework import serializers

from restaurants_recommendation.reviews.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "restaurant_id",
            "user_id",
            "content",
            "created_at",
            "updated_at",
        )
