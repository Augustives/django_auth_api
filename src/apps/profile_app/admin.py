from django.contrib import admin

from apps.profile_app.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile

    list_display = (
        "id",
        "document",
        "document_type",
        "name",
        "gender",
        "birth_date",
        "user_email",
        "user_type",
    )
    search_fields = (
        "id",
        "document",
        "name",
        "birth_date",
        "user__email",
        "user__user_type",
    )
    list_filter = ("gender", "document_type", "user__user_type")


admin.site.register(Profile, ProfileAdmin)
