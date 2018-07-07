from django.core.management.base import BaseCommand

from hosting.models import UserCardDetail
from membership.models import CustomUser
from utils.stripe_utils import StripeUtils


class Command(BaseCommand):
    help = '''Imports the usercard details of all customers. Created just for
              multiple card support.'''

    def handle(self, *args, **options):
        try:
            stripe_utils = StripeUtils()
            for user in CustomUser.objects.all():
                if hasattr(user, 'stripecustomer'):
                    if user.stripecustomer:
                        card_details_resp = stripe_utils.get_card_details(
                            user.stripecustomer.stripe_id
                        )
                        card_details = card_details_resp['response_object']
                        if card_details:
                            ucd = UserCardDetail.get_or_create_user_card_detail(
                                stripe_customer=user.stripecustomer,
                                card_details=card_details
                            )
                            UserCardDetail.save_default_card_local(
                                user.stripecustomer.stripe_id,
                                ucd.card_id
                            )
                            print("Saved user card details for {}".format(
                                user.email
                            ))
                        else:
                            print(" --- Could not get card details for "
                                  "{}".format(user.email))
                            print(" --- Error: {}".format(
                                card_details_resp['error']
                            ))
                else:
                    print(" === {} does not have a StripeCustomer object".format(
                        user.email
                    ))
        except Exception as e:
            print(" *** Error occurred. Details {}".format(str(e)))
