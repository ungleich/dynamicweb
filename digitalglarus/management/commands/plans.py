from django.core.management.base import BaseCommand
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_API_PRIVATE_KEY

PAYMENT_PLANS = [
    ('spontaneous', {'amount': 3500,
                     'interval': "month",
                     'name': "The Spontaneous",
                     'currency': "chf",
                     'id': "spontaneus"
                     }),
    ('committed', {
        'amount':36000,
        'interval':'year',
        'name':'The Committed',
        'currency':'chf',
        'id':'committed'
    })
]


class Command(BaseCommand):
    help = "Record payment plans for Digital Glarus on stripe"

    def handle(self, *args, **options):
        for payment_plan, data in PAYMENT_PLANS:
            try:
                res = stripe.Plan.create(**data)
            except stripe.InvalidRequestError as e:
                print(e)


