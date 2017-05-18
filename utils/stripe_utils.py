import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_API_PRIVATE_KEY


def handleStripeError(f):
    def handleProblems(*args, **kwargs):
        response = {
            'paid': False,
            'response_object': None,
            'error': None
        }
        common_message = "Currently its not possible to make payments."
        try:
            response_object = f(*args, **kwargs)
            response = {
                'response_object': response_object,
                'error': None
            }
            return response
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            response.update({'error': err['message']})
            return response
        except stripe.error.RateLimitError as e:
            response.update({'error': "Too many requests made to the API too quickly"})
            return response
        except stripe.error.InvalidRequestError as e:
            response.update({'error': "Invalid parameters"})
            return response
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            response.update({'error': common_message})
            return response
        except stripe.error.APIConnectionError as e:
            response.update({'error': common_message})
            return response
        except stripe.error.StripeError as e:
            # maybe send email
            response.update({'error': common_message})
            return response
        except Exception as e:
            # maybe send email
            response.update({'error': common_message})
            return response

    return handleProblems


class StripeUtils(object):
    CURRENCY = 'chf'
    INTERVAL = 'month'
    SUCCEEDED_STATUS = 'succeeded'

    def __init__(self):
        self.stripe = stripe

    def update_customer_token(self, customer, token):
        customer.source = token
        customer.save()

    @handleStripeError
    def update_customer_card(self, customer_id, token):
        customer = stripe.Customer.retrieve(customer_id)
        current_card_token = customer.default_source
        customer.sources.retrieve(current_card_token).delete()
        customer.source = token
        customer.save()
        credit_card_raw_data = customer.sources.data.pop()
        new_card_data = {
            'last4': credit_card_raw_data.last4,
            'brand': credit_card_raw_data.brand
        }
        return new_card_data

    def check_customer(self, id, user, token):
        customers = self.stripe.Customer.all()
        if not customers.get('data'):
            customer = self.create_customer(token, user.email)
        else:
            try:
                customer = stripe.Customer.retrieve(id)
            except stripe.InvalidRequestError:
                customer = self.create_customer(token, user.email)
                user.stripecustomer.stripe_id = customer.get('response_object').get('id')
                user.stripecustomer.save()
        return customer

    @handleStripeError
    def get_customer(self, id):
        customer = stripe.Customer.retrieve(id)
        # data = customer.get('response_object')
        return customer

    @handleStripeError
    def create_customer(self, token, email):

        customer = self.stripe.Customer.create(
            source=token,
            description='description for testing',
            email=email
        )
        return customer

    @handleStripeError
    def make_charge(self, amount=None, customer=None):
        amount = int(amount * 100)  # stripe amount unit, in cents
        charge = self.stripe.Charge.create(
            amount=amount,  # in cents
            currency=self.CURRENCY,
            customer=customer
        )
        return charge

    @handleStripeError
    def create_plan(self, amount, name, id):
        self.stripe.Plan.create(
            amount=amount,
            interval=self.INTERVAL,
            name=name,
            currency=self.CURRENCY,
            id=id)

    @handleStripeError
    def make_payment(self, user, amount, token):
        charge = self.stripe.Charge.create(
            amount=amount,  # in cents
            currency=self.CURRENCY,
            customer=customer
        )
        return charge

    @handleStripeError
    def create_plan(self, amount, name, id):
        self.stripe.Plan.create(
            amount=amount,
            interval=self.INTERVAL,
            name=name,
            currency=self.CURRENCY,
            id=id)



