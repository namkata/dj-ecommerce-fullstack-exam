from django.db import models
from django.utils.translation import gettext_lazy as _
from auths.models import User, AuditMixin


class ProductView(AuditMixin):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        help_text=_("Product that was viewed"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("User who viewed the product (if authenticated)"),
    )
    timestamp = models.DateTimeField(auto_now_add=True, help_text=_("Time of the product view"))

    class Meta:
        verbose_name = _("Product View")
        verbose_name_plural = _("Product Views")
        ordering = ["-timestamp"]

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} viewed {self.product}"


class CartAbandonment(AuditMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("User who abandoned the cart"),
    )
    cart_items = models.JSONField(
        help_text=_("Stores cart items as JSON, including product IDs, quantities, etc.")
    )
    abandoned_at = models.DateTimeField(auto_now_add=True, help_text=_("Time the cart was abandoned"))

    class Meta:
        verbose_name = _("Cart Abandonment")
        verbose_name_plural = _("Cart Abandonments")
        ordering = ["-abandoned_at"]

    def __str__(self):
        user_display = self.user.username if self.user else "Guest"
        return f"Abandoned cart by {user_display}"


class SalesReport(AuditMixin):
    date = models.DateField(
        unique=True, help_text=_("The date for which the sales report is generated")
    )
    total_orders = models.IntegerField(
        default=0, help_text=_("Total number of orders placed on this date")
    )
    total_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text=_("Total revenue generated on this date"),
    )
    total_customers = models.IntegerField(
        default=0, help_text=_("Total number of unique customers on this date")
    )

    class Meta:
        verbose_name = _("Sales Report")
        verbose_name_plural = _("Sales Reports")
        ordering = ["-date"]

    def __str__(self):
        return f"Sales Report - {self.date}: {self.total_orders} orders, ${self.total_revenue}"


class BestSellingProduct(AuditMixin):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        help_text=_("The best-selling product"),
    )
    total_sold = models.IntegerField(
        default=0, help_text=_("Total number of units sold")
    )
    last_updated = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    class Meta:
        verbose_name = _("Best Selling Product")
        verbose_name_plural = _("Best Selling Products")
        ordering = ["-total_sold"]

    def __str__(self):
        return f"{self.product.name} - {self.total_sold} sold"
