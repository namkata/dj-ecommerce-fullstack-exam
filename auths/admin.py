from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAddress, PhoneNumber, PhoneVerification
from django.utils import timezone


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "default_phone_number",
                    "profile_picture",
                    "date_of_birth",
                    "gender",
                )
            },
        ),
        (
            "E-commerce Info",
            {"fields": ("default_address", "wallet_balance", "loyalty_points")},
        ),
        ("Preferences", {"fields": ("newsletter_subscribed", "preferred_language")}),
    )
    list_display = (
        "username",
        "email",
        "get_phone_number",
        "get_phone_verified",
        "is_active",
        "is_staff",
    )
    search_fields = ("username", "email", "default_phone_number__phone_number")
    list_filter = ("is_active", "is_staff")

    def get_phone_number(self, obj):
        return (
            obj.default_phone_number.phone_number if obj.default_phone_number else None
        )

    get_phone_number.short_description = "Phone Number"

    def get_phone_verified(self, obj):
        return (
            obj.default_phone_number.is_phone_verified
            if obj.default_phone_number
            else False
        )

    get_phone_verified.boolean = True
    get_phone_verified.short_description = "Phone Verified"


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "is_primary", "is_phone_verified")
    search_fields = ("user__username", "phone_number")
    list_filter = ("is_primary", "is_phone_verified")


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address_line1", "city", "country")
    search_fields = ("user__username", "address_line1", "city", "country")


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "otp",
        "created_at",
        "expires_at",
        "is_expired",
    )
    search_fields = ("user__username", "phone_number__phone_number", "otp")
    list_filter = ("created_at", "expires_at")

    def is_expired(self, obj):
        return obj.expires_at < timezone.now()

    is_expired.boolean = True
    is_expired.short_description = "Expired"
