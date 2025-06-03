from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        listing_id = self.kwargs['listing_id']
        return Review.objects.filter(listing_id=listing_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

