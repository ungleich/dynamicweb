# import re

# from django.test import TestCase
# from django.core.urlresolvers import reverse
# from django.core import mail


# class LoginTestCase(TestCase):
#     def test_login(self):
#         url = reverse('login_glarus')
#         res = self.client.post(
#             url,
#             data={
#                 'email': 'test@gmail.com',
#                 'password': 'test', 'name':
#                 'test'}
#         )
#         self.assertContains(res, "You\'re successfully registered!", 1, 200)
#         self.assertEqual(len(mail.outbox), 1)
#
#         validation_url = re.findall(r"http://.*?(/.*)", mail.outbox[0].body)
#         res1 = self.client.get(validation_url[0] + '/')
#         self.assertContains(res1, "Email verified!", 1, 200)
#
#         res2 = self.client.post(
#             url, data={'email': 'test@gmail.com', 'password': 'test'}
#         )
#         self.assertEqual(res2.status_code, 302)
#         redirect_location = res2.get('Location')
#
#         res3 = self.client.get(redirect_location)
#         self.assertContains(res3, 'Pick coworking date.', 1, 200)
#
#         # check fail login
#
#         res4 = self.client.post(
#             url, data={
#                 'email': 'test@gmail.com', 'password': 'falsepassword'
#             }
#         )
#         self.assertContains(res4, 'Sorry, that login was invalid.', 1, 200)
