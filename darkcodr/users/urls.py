from django.urls import path

from darkcodr.users.views import (
    user_detail_view,
    user_redirect_view,

    # update views
    user_update_view,
    user_update_company_view,

    # hx-get views
    user_add_card,
    check_card,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~update/company/", view=user_update_company_view, name="update-company"),
    path("~add/card/", view=user_add_card, name="add-card"),
    path("~check/card/", view=check_card, name="check-card"),

    path("<str:username>/", view=user_detail_view, name="detail"),
]
