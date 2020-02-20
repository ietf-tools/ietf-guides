from django.core.management.base import BaseCommand

from guides.factories import ParticipantFactory, GuideFactory

class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(10):
            ParticipantFactory()
        for _ in range(10):
            GuideFactory()
