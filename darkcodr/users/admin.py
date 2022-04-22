from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from darkcodr.utils.export_as_csv import ExportCsvMixin

from darkcodr.users.forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Profile, CardDetail

User = get_user_model()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', 'phone', 'office_phone', 'office_address', 'city', 'country', 'postcode', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('user', 'phone', 'office_phone', 'office_address', 'city', 'country', 'postcode')

    actions = [
        "export_as_csv",
    ]



@admin.register(CardDetail)
class CardDetailAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', 'card_number', 'card_type', 'card_expiry_year', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('user', 'card_number', 'card_type')

    actions = [
        "export_as_csv",
    ]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ExportCsvMixin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "country_of_origin", "unique_id")}),
        (_("Points info"), {"fields": ("points", "first_purchase")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "subscribe_newsletter",
                    "accept_terms",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "email", "country_of_origin", "unique_id", "is_superuser"]
    search_fields = ["name", "email", "country_of_origin", "unique_id",]
    list_filter = ["country_of_origin", "is_superuser", "subscribe_newsletter",
                    "accept_terms", "is_active"]

    actions = [
        "export_as_csv",
    ]

    # def save_model(self, request, obj, form, change):
    #     user = request.user
    #     if change and form.is_valid():
    #         obj.admin = user
    #         obj.save()
    #     super().save_model(request, obj, form, change)

