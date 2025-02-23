from django.db import models
from auths.models import User, AuditMixin
from django.utils.translation import gettext_lazy as _

class ContactMessage(AuditMixin):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name="contact_messages",
        help_text=_("The user who submitted this message (if logged in).")
    )
    name = models.CharField(
        max_length=255, help_text=_("Full name of the person submitting the message.")
    )
    email = models.EmailField(
        help_text=_("Email address of the sender.")
    )
    subject = models.CharField(
        max_length=255, help_text=_("Short subject of the message.")
    )
    message = models.TextField(
        help_text=_("The content of the message.")
    )
    is_resolved = models.BooleanField(
        default=False, help_text=_("Indicates whether the message has been handled.")
    )

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
