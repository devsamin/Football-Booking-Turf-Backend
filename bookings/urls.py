# bookings/urls.py
from django.urls import path
from .views import BookingCreateView, MyBookingListView,  create_payment,payment_success,payment_fail
from .views import bookings_by_date
urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking-create"),
    path("my-bookings/", MyBookingListView.as_view(), name="my-bookings"),
    path("by-date/", bookings_by_date),

    path("create-payment/", create_payment),
    path("payment-success/", payment_success),
    path("payment-fail/", payment_fail),


]
