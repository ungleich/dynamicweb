from django.test import TestCase
from django.test import Client
from model_mommy import mommy


class BaseTestCase(TestCase):
    """
    Base class to initialize the test cases
    """

    def setUp(self):

        # Password
        self.dummy_password = 'test_password'

        # Users
        self.customer, self.another_customer = mommy.make('membership.CustomUser',
                                                          _quantity=2)
        self.customer.set_password(self.dummy_password)
        self.customer.save()
        self.another_customer.set_password(self.dummy_password)
        self.another_customer.save()

        # Stripe mocked data
        self.stripe_mocked_customer = self.customer_stripe_mocked_data()

        #  Clients
        self.customer_client = self.get_client(self.customer)
        self.another_customer_client = self.get_client(self.another_customer)

    def get_client(self, user):
        """
        Authenticate a user and return the client
        """
        client = Client()
        client.login(email=user.email, password=self.dummy_password)
        return client

    def customer_stripe_mocked_data(self):
        return {
            "id": "cus_8R1y9UWaIIjZqr",
            "object": "customer",
            "currency": "usd",
            "default_source": "card_18A9up2eZvKYlo2Cq2RJMGeF",
            "email": "vmedixtodd+1@gmail.com",
            "livemode": False,
            "metadata": {
            },
            "shipping": None,
            "sources": {
                "object": "list",
                "data": [{
                    "id": "card_18A9up2eZvKYlo2Cq2RJMGeF",
                    "object": "card",
                    "brand": "Visa",
                    "country": "US",
                    "customer": "cus_8R1y9UWaIIjZqr",
                    "cvc_check": "pass",
                    "dynamic_last4": None,
                    "exp_month": 12,
                    "exp_year": 2018,
                    "funding": "credit",
                    "last4": "4242",
                }]
            }
        }
