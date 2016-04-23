import stripe
from django.conf import settings


class StripeUtils(object):

    CURRENCY = 'chf'
    INTERVAL = 'month'
    SUCCEEDED_STATUS = 'succeeded'

    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_API_PRIVATE_KEY

    def create_plan(self, amount, name, id):
        self.stripe.Plan.create(
          amount=amount,
          interval=self.INTERVAL,
          name=name,
          currency=self.CURRENCY,
          id=id)

    def make_payment(self, user, amount, token, time):
        try:
            # Use Stripe's library to make requests...
            charge = self.stripe.Charge.create(
                amount=amount,
                currency=self.CURRENCY,
                source=token,
                description=settings.STRIPE_DESCRIPTION_ON_PAYMENT
            )

            if charge.get('status') == self.SUCCEEDED_STATUS:
                # do something
                pass
            return charge['status']
        except self.stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            return err['message']
        except self.stripe.error.RateLimitError as e:
            return "Too many requests made to the API too quickly"
        except self.stripe.error.InvalidRequestError as e:
            return "Invalid parameters"
        except self.stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except self.stripe.error.APIConnectionError as e:
            return "Currently its not possible to make payments."
        except self.stripe.error.StripeError as e:
            # maybe send email
            return "Currently its not possible to make payments."
        except Exception as e:
            # maybe send email
            return "Currently its not possible to make payments."
