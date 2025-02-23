from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "created_at")
    search_fields = ("cart__user__username", "product__name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    search_fields = ("user__username", "id")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    actions = ["mark_as_shipped"]

    def mark_as_shipped(self, request, queryset):
        """Hành động đánh dấu đơn hàng là 'Shipped'"""
        queryset.update(status=Order.OrderStatus.SHIPPED)

    mark_as_shipped.short_description = "Mark selected orders as Shipped"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "created_at")
    search_fields = ("order__id", "product__name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
