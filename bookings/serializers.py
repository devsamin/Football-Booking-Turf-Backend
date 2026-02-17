# # bookings/serializers.py
# from rest_framework import serializers
# from .models import Booking

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = "__all__"
#         read_only_fields = ["user", "status", "created_at"]


from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["user", "status", "created_at"]

    def validate(self, data):
        if Booking.objects.filter(
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            status__in=["pending", "confirmed"]
        ).exists():
            raise serializers.ValidationError(
                "এই সময়ের স্লট ইতিমধ্যে বুক করা হয়েছে।"
            )
        return data
