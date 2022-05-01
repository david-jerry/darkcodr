from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "darkcodr.core"
    verbose_name = _("Core Apps")

    def ready(self):
        try:
            import darkcodr.core.signals  # noqa F401
        except ImportError:
            pass
