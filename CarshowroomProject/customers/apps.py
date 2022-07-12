from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from core import signals
        from core.models import BaseUser
        # Explicitly connect a signal handler.
        signals.post_save.connect(signals.update_customer_signal, sender=BaseUser)