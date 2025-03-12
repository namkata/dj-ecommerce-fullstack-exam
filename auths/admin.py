from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress, PhoneNumber, PhoneVerification
from django.utils import timezone


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Additional Info"),
            {
                "fields": (
                    "default_phone_number",
                    "profile_picture",
                    "date_of_birth",
                    "gender",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("E-commerce Info"),
            {
                "fields": ("default_address", "wallet_balance", "loyalty_points"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Preferences"),
            {"fields": ("newsletter_subscribed", "preferred_language"), "classes": ("collapse",)},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        "username",
        "email",
        "get_full_name",
        "get_phone_number",
        "get_phone_verified",
        "wallet_balance",
        "is_active",
        "is_staff",
    )
    list_select_related = ("default_phone_number", "default_address")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "default_phone_number__phone_number",
        "default_address__address_line1",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "gender",
        "preferred_language",
        "newsletter_subscribed",
        "date_joined",
    )
    ordering = ("-date_joined",)
    autocomplete_fields = ["default_phone_number", "default_address"]
    readonly_fields = ("last_login", "date_joined")
    save_on_top = True

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = _("Full Name")

    def get_phone_number(self, obj):
        if not obj.default_phone_number:
            return None
        return format_html(
            '<span style="white-space: nowrap;">{}</span>',
            obj.default_phone_number.phone_number
        )
    get_phone_number.short_description = _("Phone Number")
    get_phone_number.admin_order_field = "default_phone_number__phone_number"

    def get_phone_verified(self, obj):
        return (
            obj.default_phone_number.is_phone_verified
            if obj.default_phone_number
            else False
        )
    get_phone_verified.boolean = True
    get_phone_verified.short_description = _("Phone Verified")
    get_phone_verified.admin_order_field = "default_phone_number__is_phone_verified"

    def changelist_view(self, request, extra_context=None):
        """Override to add custom CSS for wallet balance formatting"""
        extra_context = extra_context or {}
        extra_context['custom_css'] = """
            <style>
                .field-wallet_balance { white-space: nowrap; }
                .positive-balance { color: green; }
            </style>
        """
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Add annotation for formatted wallet balance display"""
        qs = super().get_queryset(request)
        return qs.select_related('default_phone_number', 'default_address')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "is_primary", "is_phone_verified", "created_at")
    list_filter = ("is_primary", "is_phone_verified", "created_at")
    search_fields = ["phone_number", "user__username", "user__email", "user__first_name", "user__last_name"]
    autocomplete_fields = ["user"]
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    save_on_top = True


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "get_full_address", "phone_number", "is_default", "is_active")
    list_filter = ("country", "city", "is_default", "is_active", "created_at")
    search_fields = [
        "address_line1",
        "address_line2",
        "city",
        "state",
        "country",
        "postal_code",
        "user__username",
        "user__email",
    ]
    autocomplete_fields = ["user", "phone_number"]
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    save_on_top = True

    def get_full_address(self, obj):
        address_parts = [obj.address_line1]
        if obj.address_line2:
            address_parts.append(obj.address_line2)
        address_parts.extend([obj.city, obj.state, str(obj.country.name), obj.postal_code])
        return ", ".join(filter(None, address_parts))
    get_full_address.short_description = _("Full Address")


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "otp",
        "created_at",
        "expires_at",
        "is_expired",
        "is_used",
    )
    search_fields = (
        "user__username",
        "user__email",
        "phone_number__phone_number",
        "otp",
    )
    list_filter = ("is_used", "created_at", "expires_at")
    autocomplete_fields = ["user", "phone_number"]
    readonly_fields = ("created_at", "expires_at")
    ordering = ("-created_at",)
    save_on_top = True

    def is_expired(self, obj):
        is_expired = obj.expires_at < timezone.now()
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if is_expired else 'green',
            'Yes' if is_expired else 'No'
        )
    is_expired.short_description = _("Expired")
    is_expired.admin_order_field = "expires_at"
