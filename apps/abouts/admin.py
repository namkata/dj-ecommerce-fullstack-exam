from django.contrib import admin
from apps.abouts.models import About


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title", "content")
