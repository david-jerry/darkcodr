from django.urls import path

from .views import notification_list

app_name = "notif"
urlpatterns = [
    # Chat view urls
    path("", view=notification_list, name="list"),
    # path("<int:user_id>/", view=message_view, name="message"),

    # # Chat app APIs
    # path("api/add_message/", view=api_add_message, name="add_message"),
    # path("api/add_chat_like/", view=chat_like_api, name="add_chat_like_api"),
]
