from django.apps import AppConfig

# from app.db_config import load_health_dbs


class HealthcheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthcheck'

    # def ready(self):
    #     load_health_dbs()
