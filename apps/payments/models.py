from django.db import models
from apps.orders.models import Order
from auths.models import AuditMixin, User
from django.utils.translation import gettext_lazy as _


class Payment(AuditMixin):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = "Credit Card", _("Credit Card")
        PAYPAL = "PayPal", _("PayPal")
        COD = "Cash on Delivery", _("Cash on Delivery")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        help_text=_("The user who made this payment."),
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
        help_text=_("The order associated with this payment."),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("The total amount paid for the order."),
    )
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        help_text=_("The payment method used for this transaction."),
    )

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.amount} {self.method}"


class Transaction(AuditMixin):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text=_("The payment associated with this transaction."),
    )
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("The unique identifier for this transaction."),
    )
    status = models.CharField(
        max_length=50,
        help_text=_(
            "The current status of the transaction (e.g., Completed, Pending, Failed)."
        ),
    )

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
