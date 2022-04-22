from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'darkcodr.notifications'

    def ready(self):
        try:
            import darkcodr.notifications.signals  # noqa F401
        except ImportError:
            pass
