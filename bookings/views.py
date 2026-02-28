# # bookings/views.py
# from rest_framework import generics, permissions
# from .models import Booking
# from .serializers import BookingSerializer

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Booking

# class BookingCreateView(generics.CreateAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class MyBookingListView(generics.ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(user=self.request.user).order_by("-created_at")




# @api_view(['GET'])
# def bookings_by_date(request):
#     date = request.GET.get("date")

#     bookings = Booking.objects.filter(
#         date=date,
#         status__in=["pending", "confirmed"]   # cancelled যেন block না করে
#     )

#     data = [
#         {
#             "start_time": b.start_time.strftime("%H:%M"),
#             "end_time": b.end_time.strftime("%H:%M"),
#         }
#         for b in bookings
#     ]

#     return Response(data)



# from sslcommerz_lib import SSLCOMMERZ
# from django.conf import settings
# from uuid import uuid4
# from datetime import datetime
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes


# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def create_payment(request):

#     total_amount = request.data.get("total")
#     slots = request.data.get("slots")
#     date = request.data.get("date")

#     transaction_id = str(uuid4())

#     settings_dict = {
#         'store_id': settings.SSLC_STORE_ID,
#         'store_pass': settings.SSLC_STORE_PASS,
#         'issandbox': True
#     }

#     sslcz = SSLCOMMERZ(settings_dict)

#     # 🔥 Create temporary booking first
#     for slot in slots:
#         start, end = slot.split("-")

#         # 🔥 Backend price calculate
#         if start in ["06:00", "07:00"]:
#             price = 1000
#         elif start in ["08:00", "09:00"]:
#             price = 1200
#         else:
#             price = 1500

#         Booking.objects.create(
#             user=request.user,
#             date=date,
#             start_time=start,
#             end_time=end,
#             price=price,  # ✅ MUST
#             payment_method="online",
#             payment_status="unpaid",
#             status="pending",
#             transaction_id=transaction_id
#         )

#     post_body = {
#         'total_amount': total_amount,
#         'currency': "BDT",
#         'tran_id': transaction_id,
#         'success_url': "http://127.0.0.1:8000/api/bookings/payment-success/",
#         'fail_url': "http://127.0.0.1:8000/api/bookings/payment-fail/",
#         'cancel_url': "http://127.0.0.1:8000/api/bookings/payment-fail/",
#         'cus_name': request.user.username,
#         'cus_email': request.user.email,
#         'cus_phone': "01700000000",
#         'product_name': "Field Booking",
#         'product_category': "Booking",
#         'product_profile': "general",
#     }

#     response = sslcz.createSession(post_body)

#     if response.get("status") != "SUCCESS":
#         return Response({"error": "Payment session failed"}, status=400)

#     return Response({
#         "payment_url": response["GatewayPageURL"]
#     })


# # ✅ PAYMENT SUCCESS
# @api_view(["POST"])
# def payment_success(request):

#     transaction_id = request.data.get("tran_id")

#     bookings = Booking.objects.filter(transaction_id=transaction_id)

#     for booking in bookings:
#         booking.payment_status = "paid"
#         booking.status = "confirmed"
#         booking.save()

#     return Response({"message": "Payment successful"})


# # ❌ PAYMENT FAIL / CANCEL
# @api_view(["POST"])
# def payment_fail(request):

#     transaction_id = request.data.get("tran_id")

#     Booking.objects.filter(transaction_id=transaction_id).delete()

#     return Response({"message": "Payment failed, booking cancelled"})





from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from uuid import uuid4
from sslcommerz_lib import SSLCOMMERZ
from .models import Booking
from .serializers import BookingSerializer

# -----------------------------
# Booking Create (Cash Booking)
# -----------------------------
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        start = serializer.validated_data["start_time"]

        # Backend price calculation
        if start.strftime("%H:%M") in ["06:00", "07:00"]:
            price = 1000
        elif start.strftime("%H:%M") in ["08:00", "09:00"]:
            price = 1200
        else:
            price = 1500

        serializer.save(
            user=self.request.user,
            price=price,
            payment_method="cash",
            payment_status="unpaid"
        )

# -----------------------------
# List My Bookings
# -----------------------------
class MyBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")


# -----------------------------
# Bookings by Date (API)
# -----------------------------
@api_view(['GET'])
def bookings_by_date(request):
    date = request.GET.get("date")

    bookings = Booking.objects.filter(
        date=date,
        status__in=["pending", "confirmed"]  # cancelled block হবে না
    )

    data = [
        {
            "start_time": b.start_time.strftime("%H:%M"),
            "end_time": b.end_time.strftime("%H:%M"),
        }
        for b in bookings
    ]

    return Response(data)


# -----------------------------
# Online Payment (SSLCommerz)
# -----------------------------
frontend_base_url = "http://localhost:5173" 
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_payment(request):
    total_amount = request.data.get("total")
    slots = request.data.get("slots")
    date = request.data.get("date")

    transaction_id = str(uuid4())

    settings_dict = {
        'store_id': settings.SSLC_STORE_ID,
        'store_pass': settings.SSLC_STORE_PASS,
        'issandbox': True
    }

    sslcz = SSLCOMMERZ(settings_dict)

    # Temporary booking creation
    for slot in slots:
        start, end = slot.split("-")

        # Backend price calculate
        if start in ["06:00", "07:00"]:
            price = 1000
        elif start in ["08:00", "09:00"]:
            price = 1200
        else:
            price = 1500

        Booking.objects.create(
            user=request.user,
            date=date,
            start_time=start,
            end_time=end,
            price=price,          # MUST
            payment_method="online",
            payment_status="unpaid",
            status="pending",
            transaction_id=transaction_id
        )

    # SSLCommerz payload
    post_body = {
        'total_amount': total_amount,
        'currency': "BDT",
        'tran_id': transaction_id,
        'success_url': f"{frontend_base_url}/payment-success?tran_id={transaction_id}",
        'fail_url': f"{frontend_base_url}/booking?payment=failed&tran_id={transaction_id}",
        'cancel_url': f"{frontend_base_url}/booking?payment=cancel&tran_id={transaction_id}",

        'cus_name': request.user.username,
        'cus_email': request.user.email,
        'cus_phone': "01700000000",
        'product_name': "Field Booking",
        'product_category': "Booking",
        'product_profile': "general",
    }

    response = sslcz.createSession(post_body)

    if response.get("status") != "SUCCESS":
        return Response({"error": "Payment session failed"}, status=400)

    return Response({
        "payment_url": response["GatewayPageURL"]
    })


# -----------------------------
# Payment Success
# -----------------------------
@api_view(["POST"])
def payment_success(request):
    transaction_id = request.data.get("tran_id")
    bookings = Booking.objects.filter(transaction_id=transaction_id)

    for booking in bookings:
        booking.payment_status = "paid"
        booking.status = "confirmed"
        booking.save()

    return Response({"message": "Payment successful"})


# -----------------------------
# Payment Fail / Cancel
# -----------------------------
@api_view(["POST"])
def payment_fail(request):
    transaction_id = request.data.get("tran_id")
    Booking.objects.filter(transaction_id=transaction_id).delete()

    return Response({"message": "Payment failed, booking cancelled"})