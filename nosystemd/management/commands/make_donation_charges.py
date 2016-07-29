from django.core.management.base import BaseCommand

from datetime import datetime

from utils.stripe_utils import StripeUtils

from nosystemd.models import DonatorStatus, Donation
from nosystemd.forms import DonationForm


class Command(BaseCommand):
    help = 'Make the monthly stripe charge to all donators'
    CURRENCY = 'usd'

    def handle(self, *args, **options):
        donators = DonatorStatus.objects.filter(status=DonatorStatus.ACTIVE)
        current_month = datetime.now().month
        current_year = datetime.now().year

        print("--------- STARTING DONATIONS SCRIPT  ---------")
        print("Donations date: %s-%s" % (current_month, current_year))

        for donator_status in donators:
            donator = donator_status.user.stripecustomer
            try:
                Donation.objects.get(created_at__month=current_month,
                                     created_at__year=current_year,
                                     donator=donator)
            except Donation.DoesNotExist:
                try:
                    # Get donator last donation amount
                    last_donation = Donation.objects.filter(donator=donator).last()
                    donation_amount = last_donation.donation

                    # Make stripe charge to a customer
                    stripe_utils = StripeUtils()
                    stripe_utils.CURRENCY = self.CURRENCY
                    charge_response = stripe_utils.make_charge(amount=donation_amount,
                                                               customer=donator.stripe_id)
                    charge = charge_response.get('response_object')

                    # Check if the payment was approved
                    if not charge:
                        # There is an error trying to creating the stripe charge
                        context = {
                            'paymentError': charge_response.get('error'),
                        }
                        print("--------- STRIPE PAYMENT ERROR ---------")
                        print(context)
                        print("-------------------------")
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
                        print("--------- PAYMENT DONATION SUCCESSFULL ---------")
                        print("Donator: %s" % donation.donator.user.email)
                        print("Amount: %s %s" % (donation.donation, self.CURRENCY))
                        print("-----------------------------------------------")
                except Exception as e:
                    print("--------- ERROR ---------")
                    print(e)
                    print("-------------------------")
                    continue
