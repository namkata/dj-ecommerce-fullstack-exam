from django.db import models
from django.utils.translation import gettext_lazy as _
from auths.models import AuditMixin


class Category(AuditMixin):
    name = models.CharField(max_length=255, unique=True, help_text=_("Category name"))
    slug = models.SlugField(unique=True, help_text=_("Unique URL-friendly identifier"))
    description = models.TextField(
        blank=True, null=True, help_text=_("Category description")
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        help_text=_("Select a parent category if this is a subcategory (optional)."),
    )
    icons = models.ImageField(
        verbose_name=_("Icons"), 
        null=True,
        blank=True, 
        upload_to='category_icons',
        help_text=_("Select a icon if this need icon show (optional).")
        )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
