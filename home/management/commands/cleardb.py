from django.core.management.base import BaseCommand
from home.models import Aliment

class Command(BaseCommand):
    """Clear the aliment table."""
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Aliment.objects.all().delete()