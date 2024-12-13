from django.apps import AppConfig

class PesananConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pesanan"

    def ready(self):
        import pesanan.signals  # Pastikan signal di-load
