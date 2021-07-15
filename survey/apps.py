from django.apps import AppConfig


class SurveyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'survey'

    def ready(self):
        super().ready()
        from .signals import update_ranking
