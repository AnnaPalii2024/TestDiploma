from enum import Enum

from django.db import models

from django.db import models
from django.utils import timezone

from user.models import CustomUser

class RoomType(str, Enum):
    SINGLE_ROOM = "Одна комната (студия)"
    ONE_BEDROOM = "Одна комната с отдельной спальней"
    TWO_BEDROOM = "Две комнаты с общей ванной"
    TWO_BEDROOM_ENSUITE = "Две комнаты с отдельными ванными"
    THREE_BEDROOM = "Три комнаты"
    SUITE = "Сьют / Апартаменты"
    SHARED_ROOM = "Общая комната / койко-место"
    PRIVATE_ROOM_IN_SHARED = "Отдельная комната в общей квартире"
    LOFT = "Лофт / Мансарда"
    STUDIO = "Студия"
    HAUS = "Дом"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    rooms_count = models.PositiveSmallIntegerField(default=0)
    room_type = models.CharField(max_length=36, choices=RoomType.choices(),default=RoomType.SINGLE_ROOM)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings"
    )

    def __str__(self):
        return self.title

