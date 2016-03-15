import unittest
from django.test import TestCase,Client

# Create your tests here.
class LoginTestCase(unittest.TestCase):
    def test_login(self):
        client = Client()
        response = client.get("/login")





