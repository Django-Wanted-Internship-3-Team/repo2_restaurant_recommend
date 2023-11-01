from django.db import models
from django.db.models import Q


class Review(models.Model):
    rating = models.FloatField(default=0)
    content = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "reviews"
        constraints = [
            models.CheckConstraint(check=(Q(rating__gte=0) & Q(rating__lte=5)), name="rating_0_to_5_constraint"),
        ]

    def __str__(self):
        return f"[{self.restaurant.business_name} - {self.user.username}]: {self.content}"
