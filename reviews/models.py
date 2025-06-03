from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1–5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listing', 'user')  # один отзыв от пользователя

    def __str__(self):
        return f"{self.user.email} → {self.listing.title} ({self.rating})"
