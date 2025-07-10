from django.core.management.base import BaseCommand
from datetime import datetime, timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class Command(BaseCommand):
    help = "Clean expired JWT tokens from the database"

    def handle(self, *args, **options):
        count, _ = OutstandingToken.objects.filter(expires_at__lt=datetime.now(timezone.utc)).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} expired tokens"))
