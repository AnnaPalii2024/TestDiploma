from django.db.models import Q, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import BasePermission, SAFE_METHODS

from django_filters import rest_framework as filters

from listings.models import Listing
from listings.serializer import RentListSerializer, RentCreateSerializer, RentDetailSerializer, \
    RentSwitchActiveSerializer


class RentFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms_min = filters.NumberFilter(field_name='rooms_count', lookup_expr='gte')
    rooms_max = filters.NumberFilter(field_name='rooms_count', lookup_expr='lte')
    owner = filters.CharFilter(field_name='owner__email', lookup_expr='icontains')

    class Meta:
        model = Listing
        fields = []

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        print(request.user.role)
        return request.user.role == "landlord"
                                     

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            print(request.user, "--------", obj.owner)
            return request.user == obj.owner and request.user.role == "landlord"
                                                                       


class IsOwnerOrReadOnlyBooking(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            return False
        else:
            return (request.user in (obj.lessee, obj.rent.owner)
                    and request.user.role in ("landlord", "tenant"))


class IsAdminOrAllowAny(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_staff
        return True

class RentListCreateGenericAPIView(ListCreateAPIView):
    # queryset = Rent.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    # filter_backends = [
    #     DjangoFilterBackend,
    #     # filters.SearchFilter,
    #     filters.OrderingFilter
    # ]
    #
    # filterset_class = RentFilter
    # # search_fields = ['title', 'description']
    # ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentListSerializer
        return RentCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Listing.objects.select_related('owner').filter(Q(owner=user) | Q(is_active=True))
        return queryset

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')

        rent = Listing.objects.filter(
            title=title,
            is_deleted=False
        )

        if rent.exists():
            raise PermissionDenied(
                f"Такое объявление уже подано"
            )

        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Объявление успешно создано',
            'data': response.data
        }, status=status.HTTP_201_CREATED)


class RentDetailUpdateDeleteGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'rent_id'

    def get_queryset(self):
        return Listing.objects.select_related('owner')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentDetailSerializer
        else:
            return RentCreateSerializer

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user and not obj.is_active:
            raise PermissionDenied("Объявление не доступно")
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        # serializer = RentCreateSerializer(instance=instance, data=data, partial=True)
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
