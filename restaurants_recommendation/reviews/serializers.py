from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from restaurants_recommendation.restaurants.models import Restaurant
from restaurants_recommendation.reviews.models import Review
from restaurants_recommendation.users.models import User


class ReviewListSerializer(serializers.ModelSerializer):
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


class ReviewSerializer(ModelSerializer):
    restaurant = PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    user = PrimaryKeyRelatedField(queryset=User.objects.all())

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

    def create(self, validated_data):
        restaurant = validated_data["restaurant"]
        count = Review.objects.filter(restaurant_id=validated_data["restaurant"]).count()

        review = super().create(validated_data)

        restaurant.rating = (restaurant.rating * count + review.rating) / (count + 1)
        restaurant.save()

        return review
