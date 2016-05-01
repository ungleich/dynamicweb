import stripe
from django.conf import settings
from django.db import models


stripe.api_key = settings.STRIPE_API_PRIVATE_KEY

class StripeUtils(object):
    CURRENCY = 'chf'
    INTERVAL = 'month'
    SUCCEEDED_STATUS = 'succeeded'

    def __init__(self):
        self.stripe = stripe

    def check_customer(self, id,user,token):
        customers = self.stripe.Customer.all()
        if not customers.get('data'):
            customer = self.create_customer(token,user.email)
        else:
            try:
                customer = stripe.Customer.retrieve(id)
            except stripe.InvalidRequestError:
                customer = self.create_customer(token,user.email)
                user.stripecustomer.stripe_id=customer.get('id')
                user.stripecustomer.save()
        return customer

    def create_customer(self, token, email):
        customer = stripe.Customer.create(
            source=token,
            description='description for testing',
            email=email
        )
        return customer

    def make_charge(self, amount=None, customer=None):
        amount = int(amount * 100)  # stripe amount unit, in cents
        import ipdb;ipdb.set_trace()
        try:
            charge = self.stripe.Charge.create(
                amount=amount,  # in cents
                currency=self.CURRENCY,
                customer=customer
            )
            return charge
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

    def create_plan(self, amount, name, id):
        self.stripe.Plan.create(
            amount=amount,
            interval=self.INTERVAL,
            name=name,
            currency=self.CURRENCY,
            id=id)
