from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "start_time",
        "end_time",
        "price",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)
