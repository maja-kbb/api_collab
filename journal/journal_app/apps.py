from django.apps import AppConfig


class JournalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'journal_app'

    
    def ready(self):
        import journal_app.signals