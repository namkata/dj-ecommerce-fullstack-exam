from django.contrib import admin
from apps.payments.models import Payment, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "user", "amount", "method", "created_at")
    list_filter = ("method", "created_at")
    search_fields = ("order__id", "user__username", "amount", "method")
    ordering = ("-created_at",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "payment", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("transaction_id", "payment__order__id", "status")
    ordering = ("-created_at",)
