from django.core.management.base import BaseCommand

from datetime import datetime
from django.utils import translation

from utils.stripe_utils import StripeUtils

from utils.mailer import BaseEmail
from digitalglarus.models import MembershipOrder
from digitalglarus.forms import MembershipOrderForm
# from membership.U
# from nosystemd.models import DonatorStatus, Donation
# from nosystemd.forms import DonationForm


class Command(BaseCommand):
    help = 'Make the monthly stripe charge to all donators'
    CURRENCY = 'usd'

    def handle(self, *args, **options):
        translation.activate('en-us')
        memberships_orders = MembershipOrder.objects.filter(membership__active=True)
        current_month = datetime.now().month
        current_year = datetime.now().year

        print("--------- STARTING MEMBERSHIP CHARGING SCRIPT  ---------")
        print("Memberhips date: %s-%s" % (current_month, current_year))

        for membership_order in memberships_orders:
            member = membership_order.customer
            try:
                MembershipOrder.objects.get(created_at__month=current_month,
                                            created_at__year=current_year,
                                            customer=member)
            except MembershipOrder.DoesNotExist:
                try:
                    current_membership_price = membership_order.membership.type.price

                    last_membership_order = MembershipOrder.objects.filter(customer=member).last()

                    # Make stripe charge to a customer
                    stripe_utils = StripeUtils()
                    stripe_utils.CURRENCY = self.CURRENCY
                    charge_response = stripe_utils.make_charge(amount=current_membership_price,
                                                               customer=member.stripe_id)
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
                        continue

                    # Create a donation
                    charge = charge_response.get('response_object')
                    membership_order_data = {
                        'cc_brand': charge.source.brand,
                        'stripe_charge_id': charge.id,
                        'last4': charge.source.last4,
                        'membership': last_membership_order.membership.id,
                        'billing_address': last_membership_order.billing_address.id,
                        'customer': member.id,
                        'amount': current_membership_price
                    }
                    membership_order_form = MembershipOrderForm(membership_order_data)
                    import pdb
                    pdb.set_trace()
                    if membership_order_form.is_valid():
                        membership_order = membership_order_form.save()

                        context = {
                            'order': membership_order,
                            'base_url': "{0}://{1}".format('https', 'dynamicweb.ungleich.ch')

                        }
                        email_data = {
                            'subject': 'Your monthly membership has been charged',
                            'to': member.user.email,
                            'context': context,
                            'template_name': 'membership_monthly_charge',
                            'template_path': 'digitalglarus/emails/'
                        }
                        email = BaseEmail(**email_data)
                        email.send()

                        print("--------- PAYMENT DONATION SUCCESSFULL ---------")
                        print("Member: %s" % member.user.email)
                        print("Amount: %s %s" % (current_membership_price, self.CURRENCY))
                        print("-----------------------------------------------")

                except Exception as e:
                    print("--------- ERROR ---------")
                    print(e)
                    print("-------------------------")
                    continue
        # for donator_status in donators:
        #     donator = donator_status.user.stripecustomer
        #     try:
        #         Donation.objects.get(created_at__month=current_month,
        #                              created_at__year=current_year,
        #                              donator=donator)
        #     except Donation.DoesNotExist:
        #         try:
        #             # Get donator last donation amount
        #             last_donation = Donation.objects.filter(donator=donator).last()
        #             donation_amount = last_donation.donation

        #             # Make stripe charge to a customer
        #             stripe_utils = StripeUtils()
        #             stripe_utils.CURRENCY = self.CURRENCY
        #             charge_response = stripe_utils.make_charge(amount=donation_amount,
        #                                                        customer=donator.stripe_id)
        #             charge = charge_response.get('response_object')

        #             # Check if the payment was approved
        #             if not charge:
        #                 # There is an error trying to creating the stripe charge
        #                 context = {
        #                     'paymentError': charge_response.get('error'),
        #                 }
        #                 print("--------- STRIPE PAYMENT ERROR ---------")
        #                 print(context)
        #                 print("-------------------------")
        #                 continue
        #             # Create a donation
        #             charge = charge_response.get('response_object')
        #             donation_data = {
        #                 'cc_brand': charge.source.brand,
        #                 'stripe_charge_id': charge.id,
        #                 'last4': charge.source.last4,
        #                 'billing_address': last_donation.billing_address.id,
        #                 'donator': donator.id,
        #                 'donation': donation_amount
        #             }
        #             donation_form = DonationForm(donation_data)
        #             if donation_form.is_valid():
        #                 donation = donation_form.save()

        #                 context = {
        #                     'donation': donation,
        #                     'base_url': "{0}://{1}".format('https', 'dynamicweb.ungleich.ch')

        #                 }
        #                 email_data = {
        #                     'subject': 'Your donation have been charged',
        #                     'to': donation.donator.user.email,
        #                     'context': context,
        #                     'template_name': 'donation_charge',
        #                     'template_path': 'nosystemd/emails/'
        #                 }
        #                 email = BaseEmail(**email_data)
        #                 email.send()

        #                 print("--------- PAYMENT DONATION SUCCESSFULL ---------")
        #                 print("Donator: %s" % donation.donator.user.email)
        #                 print("Amount: %s %s" % (donation.donation, self.CURRENCY))
        #                 print("-----------------------------------------------")
        #         except Exception as e:
        #             print("--------- ERROR ---------")
        #             print(e)
        #             print("-------------------------")
        #             continue
