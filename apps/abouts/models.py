from django.db import models
from django.utils.translation import gettext_lazy as _


class About(models.Model):
    title = models.CharField(max_length=255, help_text=_("Title of the about section."))
    content = models.TextField(
        help_text=_("Detailed information about the company or website.")
    )

    def __str__(self):
        return self.title
