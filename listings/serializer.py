from rest_framework import serializers

from listings.models import Listing


class RentListSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'address',
            'price',
            'rooms_count',
            'room_type',
            'owner'
        ]

class RentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'address',
            'price',
            'rooms_count',
            'room_type',
            'is_active'
        ]
        extra_kwargs = {'is_active': {'write_only': True}}


class RentDetailSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'address',
            'price',
            'rooms_count',
            'room_type',
            'is_active',
            'created_at',
            'owner'
        ]


class RentSwitchActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['is_active']