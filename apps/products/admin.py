from django.contrib import admin
from apps.products.models import Product, ProductImage, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "rating", "sold_count")
    list_filter = ("category", "rating", "stock")
    search_fields = ("name", "category__name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "alt_text")
    search_fields = ("product__name",)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    list_filter = ("user",)
    search_fields = ("user__username", "product__name")
