from django.apps import AppConfig

class UploaderConfig(AppConfig):
    name = 'uploader'

    def ready(self):
        import uploader.signals
