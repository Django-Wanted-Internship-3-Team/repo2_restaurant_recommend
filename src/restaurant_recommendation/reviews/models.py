from django.db import models


class Review(models.Model):
    rating = models.FloatField(null=True)
    content = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"[{self.restaurant.business_name} - {self.user.username}]: {self.content}"
