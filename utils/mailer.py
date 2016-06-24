import six
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from django.conf import settings


class BaseEmail(object):

    def __init__(self, *args, **kwargs):
        self.to = kwargs.get('to')
        self.template_name = kwargs.get('template_name')
        self.template_path = kwargs.get('template_path')
        self.subject = kwargs.get('subject')
        self.context = kwargs.get('context', {})
        self.template_full_path = '%s%s' % (self.template_path, self.template_name)
        text_content = render_to_string('%s.txt' % self.template_full_path, self.context)
        html_content = render_to_string('%s.html' % self.template_full_path, self.context)

        self.email = EmailMultiAlternatives(self.subject, text_content)
        self.email.attach_alternative(html_content, "text/html")
        self.email.from_email = 'no-replay@ungleich.ch'
        self.email.to = ['info@ungleich.com']

    def send(self):
        self.email.send()


class BaseMailer(object):
    def __init__(self):
        self._slug = None
        self.no_replay_mail = 'no-replay@ungleich.ch'

        if not hasattr(self, '_to'):
            self._to = None

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, val):
        assert isinstance(val, six.string_types), "slug is not string: %r" % val
        self._slug = val

    @property
    def registration(self):
        return self.message

    @registration.setter
    def registration(self, val):
        msg = "registration is not dict with fields subject,message"
        assert type(val) is dict, msg
        assert val.get('subject') and val.get('message'), msg
        self._message, self._subject, self._from = (
            val.get('message'), val.get('subject'), val.get('from'))
        assert isinstance(self.slug, six.string_types), 'slug not set'

    def send_mail(self, to=None):
        if not to:
            to = self._to
        if not self.message:
            raise NotImplementedError
        send_mail(self._subject, self._message, self.no_replay_mail, [to])


class DigitalGlarusRegistrationMailer(BaseMailer):
    message = settings.REGISTRATION_MESSAGE

    def __init__(self, slug):
        self.slug = slug
        self.registration = self.message
        self._message = self._message.format(slug=self._slug)
        super().__init__()

