from django.apps import AppConfig


class AdminAutocompleteConfig(AppConfig):
    name = 'admin_autocomplete'
    verbose_name = 'Django Admin Autocomplete'

    def ready(self):
        pass  # Add any initialization code here if needed
