from django.urls import path

from listings.views import RentListCreateGenericAPIView, RentDetailUpdateDeleteGenericAPIView

urlpatterns = [
    path('rent/', RentListCreateGenericAPIView.as_view()),
    path('rent/<int:rent_id>/', RentDetailUpdateDeleteGenericAPIView.as_view()),
]
