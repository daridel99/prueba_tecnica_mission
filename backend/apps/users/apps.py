from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        from .seed import seed_users

        def run_seed(sender, **kwargs):
            seed_users()

        post_migrate.connect(run_seed, sender=self)