# # bookings/models.py
# from django.db import models
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

# class Booking(models.Model):
#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("confirmed", "Confirmed"),
#         ("cancelled", "Cancelled"),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     price = models.PositiveIntegerField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.date} ({self.start_time}-{self.end_time})"


from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.date} ({self.start_time}-{self.end_time})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "start_time", "end_time"],
                name="unique_booking_slot"
            )
        ]
