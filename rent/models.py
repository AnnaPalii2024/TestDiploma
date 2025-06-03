from django.db import models

from rent.choices.room_type import RoomType


class Rent(models.Model):
    title = models.CharField(max_length=100)
    discription = models.TextField()
    address = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    room_count = models.PositiveSmallIntegerField()
    room_type = models.CharField(
        max_length=40,
        choices=RoomType.choices(),
    )
