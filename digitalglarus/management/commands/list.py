from django.core.management.base import BaseCommand
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_API_PRIVATE_KEY


class Command(BaseCommand):
    help = "Record payment plans for Digital Glarus on stripe"

    def handle(self, *args, **options):
        print("Available plans:")
        for plan in stripe.Plan.all():
            print(plan)
