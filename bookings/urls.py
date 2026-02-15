# bookings/urls.py
from django.urls import path
from .views import BookingCreateView, MyBookingListView
from .views import bookings_by_date
urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("my-bookings/", MyBookingListView.as_view(), name="my-bookings"),
    path("by-date/", bookings_by_date),

]
