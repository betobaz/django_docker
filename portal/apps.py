from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = 'portal'
    verbose_name = "Portal"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
