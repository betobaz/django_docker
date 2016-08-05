from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = "Api"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
