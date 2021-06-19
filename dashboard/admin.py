from django.contrib import admin
from .models import WebPa

# Register your models here.
class WebPaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "copyright_text",
        "share_info",
        "mpesa_header_depo_msg",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_editable = ("copyright_text", "share_info", "mpesa_header_depo_msg")


admin.site.register(WebPa, WebPaAdmin)
