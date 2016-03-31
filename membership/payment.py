__author__ = 'tomislav'
from django.conf import settings
from .models import CreditCards
import stripe
stripe.api_key = settings.STRIPE_API_PRIVATE_KEY


class StripePayment(object):

    @classmethod
    def make_payment(cls,user,amount,token,time):
        try:
            # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
                amount=amount,
                currency='chf',
                source=token,
                description=settings.STRIPE_DESCRIPTION_ON_PAYMENT
            )
            if charge['status'] =='succeeded':
                obj = CreditCards.objects.filter(user_id=user.id).first()
                obj.payment_type = time
                obj.save()
            return charge['status']

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            return err['message']
        except stripe.error.RateLimitError as e:
            return "Too many requests made to the API too quickly"
        except stripe.error.InvalidRequestError as e:
            return "Invalid parameters"
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
            return "Currently its not possible to make payments."
        except stripe.error.StripeError as e:
            return "Currently its not possible to make payments."
            #maybe send email
        except Exception as e:
            return "Currently its not possible to make payments."
            #maybe send email
