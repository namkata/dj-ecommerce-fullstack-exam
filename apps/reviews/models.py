from django.db import models
from apps.orders.models import Order
from apps.products.models import Product
from auths.models import AuditMixin, User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(AuditMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True,
        help_text=_("Rating from 1 to 5"),
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"Review by {self.user.username} for {self.product.name} ({self.rating} ⭐)"
        )

    @staticmethod
    def update_product_rating(product):
        """Tính toán lại điểm rating trung bình của sản phẩm"""
        reviews = product.reviews.exclude(
            rating__isnull=True
        )  # Lọc ra các đánh giá có điểm số
        avg_rating = reviews.aggregate(avg=models.Avg("rating"))["avg"]
        product.rating = avg_rating or 0
        product.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating(self.product)
