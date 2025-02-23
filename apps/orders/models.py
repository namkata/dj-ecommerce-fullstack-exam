from django.db import models
from apps.products.models import Product
from auths.models import AuditMixin, User
from django.utils.translation import gettext_lazy as _


class Cart(AuditMixin):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart", help_text=_("Cart owner")
    )

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(AuditMixin):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(
        default=1, help_text=_("Quantity of the product")
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(AuditMixin):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending", _("Pending")
        PROCESSING = "Processing", _("Processing")
        SHIPPED = "Shipped", _("Shipped")
        DELIVERED = "Delivered", _("Delivered")
        CANCELLED = "Cancelled", _("Cancelled")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text=_("The user who placed this order."),
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        help_text=_("The current status of the order."),
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_(
            "The total price of all items in the order at the time of purchase."
        ),
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        # Nếu đơn hàng được cập nhật thành SHIPPED, tạo bản ghi đánh giá
        if self.pk:  # Chỉ chạy khi cập nhật (không phải khi tạo mới)
            original = Order.objects.get(pk=self.pk)
            if original.status != "Shipped" and self.status == "Shipped":
                self.create_review_entries()
        super().save(*args, **kwargs)

    def create_review_entries(self):
        """Tạo bản ghi đánh giá cho từng sản phẩm trong đơn hàng"""
        for item in self.order_items.all():
            from apps.reviews.models import Review
            Review.objects.create(user=self.user, product=item.product, order=self)


class OrderItem(AuditMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        help_text=_("The order this item belongs to."),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        help_text=_("The product that was purchased."),
    )
    quantity = models.PositiveIntegerField(
        default=1, help_text=_("The number of units of this product in the order.")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("The price of the product at the time of purchase."),
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
