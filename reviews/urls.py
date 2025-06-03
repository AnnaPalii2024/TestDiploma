from django.urls import path
from .views import ReviewListCreateView

urlpatterns = [
    path('listings/<int:listing_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
]