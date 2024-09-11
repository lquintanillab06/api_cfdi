from django.apps import AppConfig
from . import tasks

class DescargaMasivaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.descarga_masiva"

    def ready(self) -> None:
        print("DescargaMasivaConfig ready")
        tasks.start()
    

