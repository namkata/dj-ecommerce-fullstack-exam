from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string
from datetime import timedelta
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def get_gender_choices():
    return [("Male", _("Male")), ("Female", _("Female")), ("Other", _("Other"))]


def get_language_choices():
    return [("en", _("English")), ("vi", _("Vietnamese"))]


class User(AbstractUser):
    default_phone_number = models.ForeignKey(
        "PhoneNumber",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_user",
        help_text=_("User's default phone number."),
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        help_text=_("User's profile picture."),
    )
    date_of_birth = models.DateField(
        null=True, blank=True, help_text=_("User's date of birth (YYYY-MM-DD).")
    )
    gender = models.CharField(
        max_length=10,
        choices=get_gender_choices(),
        null=True,
        blank=True,
        help_text=_("User's gender."),
    )

    default_address = models.ForeignKey(
        "UserAddress",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_user",
        help_text=_("User's default address."),
    )
    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text=_("User's wallet balance (currency: VND)."),
    )
    loyalty_points = models.PositiveIntegerField(
        default=0, help_text=_("User's accumulated loyalty points.")
    )
    newsletter_subscribed = models.BooleanField(
        default=True, help_text=_("Is the user subscribed to email newsletters?")
    )
    preferred_language = models.CharField(
        max_length=10,
        choices=get_language_choices(),
        default="en",
        help_text=_("User's preferred language."),
    )
    
    def __str__(self):
        return self.username


class AuditMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time when the record was last updated."
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        help_text="The user who created this record.",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        help_text="The user who last updated this record.",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        if request and request.user.is_authenticated:
            if not self.pk:
                self.created_by = request.user
            self.updated_by = request.user
        super().save(*args, **kwargs)


class PhoneNumber(AuditMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
        help_text=_("The user who owns this phone number."),
    )
    phone_number = models.CharField(
        max_length=15, unique=True, help_text=_("User's phone number.")
    )
    is_primary = models.BooleanField(
        default=False, help_text=_("Is this the user's primary phone number?")
    )
    
    is_phone_verified = models.BooleanField(
        default=False, help_text=_("Has the phone number been verified?")
    )


    def __str__(self):
        return f"{self.phone_number} ({'Primary' if self.is_primary else 'Secondary'})"


class UserAddress(AuditMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
        help_text=_("The user who owns this address."),
    )
    phone_number = models.ForeignKey(
        PhoneNumber,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="addresses",
        help_text=_("Phone number associated with this address."),
    )
    address_line1 = models.CharField(
        max_length=255, help_text=_("Primary address line (required).")
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Secondary address line (optional)."),
    )
    city = models.CharField(max_length=100, help_text=_("City of the address."))
    state = models.CharField(
        max_length=100, help_text=_("State/region of the address (if applicable).")
    )
    postal_code = models.CharField(
        max_length=20, help_text=_("Postal code of the address.")
    )
    country = models.CharField(max_length=100, help_text=_("Country of the address."))

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.country}"


class PhoneVerification(AuditMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="phone_verifications",
        help_text=_("User associated with OTP verification."),
    )
    phone_number = models.ForeignKey(
        PhoneNumber,
        on_delete=models.CASCADE,
        related_name="verifications",
        help_text=_("Phone number being verified."),
    )
    otp = models.CharField(
        max_length=6, help_text=_("6-digit OTP code for phone verification.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("Time when the OTP was generated.")
    )
    expires_at = models.DateTimeField(help_text=_("Expiration time of the OTP."))
    is_used = models.BooleanField(
        default=False, help_text=_("Indicates if the OTP has been used.")
    )

    def generate_otp(self):
        self.otp = "".join(random.choices(string.digits, k=6))
        self.expires_at = now() + timedelta(minutes=5)
        self.is_used = False
        self.save()

    def is_valid(self, entered_otp):
        return self.otp == entered_otp and self.expires_at > now() and not self.is_used

    def mark_as_used(self):
        self.is_used = True
        self.save()

    def __str__(self):
        status = "Used" if self.is_used else "Active"
        return f"OTP for {self.phone_number.phone_number} - {status} - Expires at {self.expires_at}"
