# bookings/urls.py
from django.urls import path
from .views import BookingCreateView, MyBookingListView

urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("my-bookings/", MyBookingListView.as_view(), name="my-bookings"),
]
