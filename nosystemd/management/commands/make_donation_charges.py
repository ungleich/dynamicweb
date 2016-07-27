from django.core.management.base import BaseCommand

from nosystem.models import DonatorStatus, Donation
from datetime import datetime

from utils.stripe_utils import StripeUtils
from .forms import DonationForm


class Command(BaseCommand):
    help = 'Make the monthly stripe charge to all donators'

    def handle(self, *args, **options):
        donators = DonatorStatus.objects.filter(status=DonatorStatus.ACTIVE)
        current_month = datetime.now().month
        current_year = datetime.now().year
        for donator in donators:
            current_month_donation = Donation.objects.get(created_at__month=current_month,
                                                          created_at__year=current_year)
            if not current_month_donation:
                last_donation = Donation.objects.filter(donator=donator).last()

                donation_amount = last_donation.donation
                # Make stripe charge to a customer
                stripe_utils = StripeUtils()
                stripe_utils.CURRENCY = 'usd'
                charge_response = stripe_utils.make_charge(amount=donation_amount,
                                                           customer=donator.stripe_id)
                charge = charge_response.get('response_object')

                # Check if the payment was approved
                if not charge:
                    # TODO save error
                    context = {
                        'paymentError': charge_response.get('error'),
                    }
                    print(context)
                # Create a donation
                charge = charge_response.get('response_object')
                donation_data = {
                    'cc_brand': charge.source.brand,
                    'stripe_charge_id': charge.id,
                    'last4': charge.source.last4,
                    'billing_address': last_donation.billing_address.id,
                    'donator': donator.id,
                    'donation': donation_amount
                }
                donation_form = DonationForm(donation_data)
                if donation_form.is_valid():
                    donation = donation_form.save()
                    print(donation)
