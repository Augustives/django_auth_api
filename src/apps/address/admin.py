from django.contrib import admin

from apps.address.models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "city", "postal_code")
    search_fields = ("country", "state", "city", "postal_code")
    list_filter = ("country", "state", "city")


admin.site.register(Address, AddressAdmin)
