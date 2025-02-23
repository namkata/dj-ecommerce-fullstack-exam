from django.db import models
from apps.categories.models import Category
from auths.models import AuditMixin, User

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(AuditMixin):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255, help_text=_("Product name"))
    slug = models.SlugField(unique=True, help_text=_("Unique URL-friendly identifier"))
    description = models.TextField(
        blank=True, null=True, help_text=_("Product description")
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text=_("Product price")
    )
    stock = models.PositiveIntegerField(
        default=0, help_text=_("Available stock quantity")
    )
    main_image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True,
        help_text=_("Main product image"),
    )
    specifications = models.JSONField(
        blank=True, null=True, help_text=_("Technical specifications")
    )
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("Product rating"),
    )
    sold_count = models.PositiveIntegerField(
        default=0, help_text=_("Total products sold")
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class ProductImage(AuditMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="product_images/", help_text=_("Additional product image")
    )
    alt_text = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Alternative text for image")
    )

    def __str__(self):
        return f"Image for {self.product.name}"


class Wishlist(AuditMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlisted_by"
    )

    class Meta:
        unique_together = ("user", "product")
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
