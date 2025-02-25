from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from auths.models import AuditMixin, User


class ShippingMethod(AuditMixin):
    name = models.CharField(max_length=100, help_text=_("Name of the shipping method (e.g., Standard, Express)"))
    carrier = models.CharField(max_length=100, help_text=_("Shipping carrier (e.g., FedEx, DHL)"))
    estimated_days = models.IntegerField(help_text=_("Estimated delivery time in days"))
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Fixed shipping fee"))
    cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Additional cost per kilogram"))
    active = models.BooleanField(default=True, help_text=_("Is this shipping method active?"))

    class Meta:
        verbose_name = _("Shipping Method")
        verbose_name_plural = _("Shipping Methods")

    def __str__(self):
        return f"{self.name} ({self.carrier})"


class ShippingAddress(AuditMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shipping_addresses",
        help_text=_("User who owns this address")
    )
    full_name = models.CharField(max_length=255, help_text=_("Full name of the recipient"))
    address_line1 = models.CharField(max_length=255, help_text=_("Street address, P.O. box, company name"))
    address_line2 = models.CharField(max_length=255, blank=True, null=True, help_text=_("Apartment, suite, unit, etc."))
    city = models.CharField(max_length=100, help_text=_("City"))
    province = models.CharField(max_length=100, blank=True, null=True, help_text=_("State or province"))
    country = CountryField(help_text=_("Country"))
    postal_code = models.CharField(max_length=20, help_text=_("ZIP or postal code"))
    phone_number = models.CharField(max_length=20, help_text=_("Contact phone number"))

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"


class Shipment(AuditMixin):
    class ShipmentStatus(models.TextChoices):
        PENDING = "Pending", _("Pending")
        SHIPPED = "Shipped", _("Shipped")
        IN_TRANSIT = "In Transit", _("In Transit")
        DELIVERED = "Delivered", _("Delivered")
        CANCELLED = "Cancelled", _("Cancelled")

    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, help_text=_("Related order"))
    shipping_method = models.ForeignKey(
        ShippingMethod, on_delete=models.SET_NULL, null=True, help_text=_("Chosen shipping method")
    )
    tracking_number = models.CharField(
        max_length=50, blank=True, null=True, help_text=_("Tracking number for shipment")
    )
    shipped_date = models.DateTimeField(blank=True, null=True, help_text=_("Date when the order was shipped"))
    delivered_date = models.DateTimeField(blank=True, null=True, help_text=_("Date when the order was delivered"))
    status = models.CharField(
        max_length=20, choices=ShipmentStatus.choices, default=ShipmentStatus.PENDING, help_text=_("Current status of the shipment")
    )

    class Meta:
        verbose_name = _("Shipment")
        verbose_name_plural = _("Shipments")

    def __str__(self):
        return f"Order {self.order.id} - {self.get_status_display()}"
