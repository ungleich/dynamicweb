import logging
import stripe
from django.conf import settings
from datacenterlight.models import StripePlan

stripe.api_key = settings.STRIPE_API_PRIVATE_KEY
logger = logging.getLogger(__name__)


def handleStripeError(f):
    def handleProblems(*args, **kwargs):
        response = {
            'paid': False,
            'response_object': None,
            'error': None
        }

        common_message = "Currently it's not possible to make payments."
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
            response.update(
                {'error': "Too many requests made to the API too quickly"})
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
    STRIPE_PLAN_ALREADY_EXISTS = 'Plan already exists'
    STRIPE_NO_SUCH_PLAN = 'No such plan'
    PLAN_EXISTS_ERROR_MSG = 'Plan {} exists already.\nCreating a local StripePlan now.'
    PLAN_DOES_NOT_EXIST_ERROR_MSG = 'Plan {} does not exist.'

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

    @handleStripeError
    def get_card_details(self, customer_id, token):
        customer = stripe.Customer.retrieve(customer_id)
        credit_card_raw_data = customer.sources.data.pop()
        card_details = {
            'last4': credit_card_raw_data.last4,
            'brand': credit_card_raw_data.brand
        }
        return card_details

    def check_customer(self, id, user, token):
        customers = self.stripe.Customer.all()
        if not customers.get('data'):
            customer = self.create_customer(token, user.email, user.name)
        else:
            try:
                customer = stripe.Customer.retrieve(id)
            except stripe.InvalidRequestError:
                customer = self.create_customer(token, user.email, user.name)
                user.stripecustomer.stripe_id = customer.get(
                    'response_object').get('id')
                user.stripecustomer.save()
        return customer

    @handleStripeError
    def get_customer(self, id):
        customer = stripe.Customer.retrieve(id)
        # data = customer.get('response_object')
        return customer

    @handleStripeError
    def create_customer(self, token, email, name=None):
        if name is None or name.strip() == "":
            name = email
        customer = self.stripe.Customer.create(
            source=token,
            description=name,
            email=email
        )
        return customer

    @handleStripeError
    def make_charge(self, amount=None, customer=None):
        _amount = float(amount)
        amount = int(_amount * 100)  # stripe amount unit, in cents
        charge = self.stripe.Charge.create(
            amount=amount,  # in cents
            currency=self.CURRENCY,
            customer=customer
        )
        return charge

    @handleStripeError
    def get_or_create_stripe_plan(self, amount, name, stripe_plan_id):
        """
        This function checks if a StripePlan with the given
        stripe_plan_id already exists. If it exists then the function
        returns this object otherwise it creates a new StripePlan and
        returns the new object.

        :param amount: The amount in CHF
        :param name: The name of the Stripe plan to be created.
        :param stripe_plan_id: The id of the Stripe plan to be
               created. Use get_stripe_plan_id_string function to
               obtain the name of the plan to be created
        :return: The StripePlan object if it exists else creates a
               Plan object in Stripe and a local StripePlan and
               returns it. Returns None in case of Stripe error
        """
        _amount = float(amount)
        amount = int(_amount * 100)  # stripe amount unit, in cents
        stripe_plan_db_obj = None
        try:
            stripe_plan_db_obj = StripePlan.objects.get(
                stripe_plan_id=stripe_plan_id)
        except StripePlan.DoesNotExist:
            try:
                self.stripe.Plan.create(
                    amount=amount,
                    interval=self.INTERVAL,
                    name=name,
                    currency=self.CURRENCY,
                    id=stripe_plan_id)
                stripe_plan_db_obj = StripePlan.objects.create(
                    stripe_plan_id=stripe_plan_id)
            except stripe.error.InvalidRequestError as e:
                if self.STRIPE_PLAN_ALREADY_EXISTS in str(e):
                    logger.debug(
                        self.PLAN_EXISTS_ERROR_MSG.format(stripe_plan_id))
                    stripe_plan_db_obj = StripePlan.objects.create(
                        stripe_plan_id=stripe_plan_id)
        return stripe_plan_db_obj

    @handleStripeError
    def delete_stripe_plan(self, stripe_plan_id):
        """
        Deletes the Plan in Stripe and also deletes the local db copy
        of the plan if it exists

        :param stripe_plan_id: The stripe plan id that needs to be
               deleted
        :return: True if the plan was deleted successfully from
               Stripe, False otherwise.
        """
        return_value = False
        try:
            plan = self.stripe.Plan.retrieve(stripe_plan_id)
            plan.delete()
            return_value = True
            StripePlan.objects.filter(
                stripe_plan_id=stripe_plan_id).all().delete()
        except stripe.error.InvalidRequestError as e:
            if self.STRIPE_NO_SUCH_PLAN in str(e):
                logger.debug(
                    self.PLAN_DOES_NOT_EXIST_ERROR_MSG.format(stripe_plan_id))
        return return_value

    @handleStripeError
    def subscribe_customer_to_plan(self, customer, plans):
        """
        Subscribes the given customer to the list of given plans

        :param customer: The stripe customer identifier
        :param plans: A list of stripe plans.
        Ref: https://stripe.com/docs/api/python#create_subscription-items
              e.g.
                    plans = [
                                {
                                  "plan": "dcl-v1-cpu-2-ram-5gb-ssd-10gb",
                                },
                            ]
        :return: The subscription StripeObject
        """

        subscription_result = self.stripe.Subscription.create(
            customer=customer,
            items=plans,
        )
        return subscription_result

    @handleStripeError
    def make_payment(self, customer, amount, token):
        charge = self.stripe.Charge.create(
            amount=amount,  # in cents
            currency=self.CURRENCY,
            customer=customer
        )
        return charge

    @staticmethod
    def get_stripe_plan_id(cpu, ram, ssd, version, app='dcl', hdd=None):
        """
        Returns the stripe plan id string of the form
        `dcl-v1-cpu-2-ram-5gb-ssd-10gb` based on the input parameters

        :param cpu: The number of cores
        :param ram: The size of the RAM in GB
        :param ssd: The size of ssd storage in GB
        :param hdd: The size of hdd storage in GB
        :param version: The version of the Stripe plans
        :param app: The application to which the stripe plan belongs
        to. By default it is 'dcl'
        :return: A string of the form `dcl-v1-cpu-2-ram-5gb-ssd-10gb`
        """
        dcl_plan_string = 'cpu-{cpu}-ram-{ram}gb-ssd-{ssd}gb'.format(cpu=cpu,
                                                                     ram=ram,
                                                                     ssd=ssd)
        if hdd is not None:
            dcl_plan_string = '{dcl_plan_string}-hdd-{hdd}gb'.format(
                dcl_plan_string=dcl_plan_string, hdd=hdd)
        stripe_plan_id_string = '{app}-v{version}-{plan}'.format(app=app,
                                                                 version=version,
                                                                 plan=dcl_plan_string)
        return stripe_plan_id_string
