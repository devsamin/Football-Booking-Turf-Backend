# bookings/views.py
from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")




@api_view(['GET'])
def bookings_by_date(request):
    date = request.GET.get("date")

    bookings = Booking.objects.filter(
        date=date,
        status__in=["pending", "confirmed"]   # cancelled যেন block না করে
    )

    data = [
        {
            "start_time": b.start_time.strftime("%H:%M"),
            "end_time": b.end_time.strftime("%H:%M"),
        }
        for b in bookings
    ]

    return Response(data)
