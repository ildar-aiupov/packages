from django.contrib import admin

from .models import Package
from .models import PackageType


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Админпанель посылок."""

    list_display = [
        "uuid",
        "name",
        "weight",
        "type",
        "content_cost",
        "delivery_cost",
        "sessionid",
    ]


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    """Админпанель типов посылок."""
    
    list_display = ["id", "name"]
    list_editable = ["name"]
