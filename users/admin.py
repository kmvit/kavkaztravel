from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SMSVerification, Booking, Notification, UserNotificationChannel

class CustomUserAdmin(UserAdmin):
    pass
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SMSVerification)

admin.site.register(UserNotificationChannel)
admin.site.register(Notification)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'payment_status', 'content_type', 'booking_date']
    list_filter = ['content_type', 'status']