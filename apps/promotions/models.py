from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from auths.models import AuditMixin


class Promotion(AuditMixin):
    class DiscountType(models.TextChoices):
        FIXED = "fixed", _("Fixed Amount")
        PERCENT = "percent", _("Percentage")

    class AppliesTo(models.TextChoices):
        PRODUCT = "product", _("Product")
        CATEGORY = "category", _("Category")
        CART = "cart", _("Entire Cart")

    name = models.CharField(max_length=100, help_text=_("Name of the promotion"))
    code = models.CharField(
        max_length=20, unique=True, help_text=_("Unique promo code (e.g., SUMMER10)")
    )
    discount_type = models.CharField(
        max_length=10, choices=DiscountType.choices, default=DiscountType.PERCENT
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, help_text=_("Discount value (fixed amount or percentage)")
    )
    applies_to = models.CharField(
        max_length=20, choices=AppliesTo.choices, default=AppliesTo.CART
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Applicable product (if any)")
    )
    category = models.ForeignKey(
        "categories.Category", on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Applicable category (if any)")
    )
    min_order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, help_text=_("Minimum order amount required")
    )
    max_uses = models.IntegerField(
        default=1, help_text=_("Maximum number of times this promo can be used")
    )
    used_count = models.IntegerField(
        default=0, help_text=_("Number of times this promo has been used")
    )
    start_date = models.DateTimeField(help_text=_("Promotion start date"))
    end_date = models.DateTimeField(help_text=_("Promotion end date"))
    active = models.BooleanField(default=True, help_text=_("Is the promotion active?"))

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

    def is_valid(self):
        return self.active and self.start_date <= now() <= self.end_date and self.used_count < self.max_uses

    def __str__(self):
        return f"{self.name} ({self.code})"


class AppliedPromotion(AuditMixin):
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, help_text=_("Order that applied this promotion")
    )
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, help_text=_("Applied promotion")
    )
    discount_applied = models.DecimalField(
        max_digits=10, decimal_places=2, help_text=_("Amount discounted")
    )

    class Meta:
        verbose_name = _("Applied Promotion")
        verbose_name_plural = _("Applied Promotions")

    def __str__(self):
        return f"Order {self.order.id} - {self.promotion.name}"
