import datetime

from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.utils.translation import get_language
from djangocms_blog.models import Post
from django.contrib import messages


from .models import Supporter
from utils.forms import ContactUsForm
from django.views.generic.edit import FormView


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('digitalglarus:contact')
    success_message = _('Message Successfully Sent')

    def form_valid(self, form):
        form.save()
        form.send_email()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(ContactView, self).form_valid(form)


class IndexView(TemplateView):
    template_name = "digitalglarus/index.html"


class AboutView(TemplateView):
    template_name = "digitalglarus/about.html"

def detail(request, message_id):
    p = get_object_or_404(Message, pk=message_id)

    context = { 'message': p, }
    return render(request, 'digitalglarus/detail.html', context)

def about(request):
    return render(request, 'digitalglarus/about.html')



#def index(request):
#    return render(request, 'digitalglarus/index.html')
#
#def letscowork(request):
#    return render(request, 'digitalglarus/letscowork.html')

# def index(request):
#     return home(request)

def home(request):
    return render(request, 'index.html')

def letscowork(request):
    return render(request, 'digitalglarus/letscowork.html')


def blog(request):
    tags = ["digitalglarus"]
    posts = Post.objects.filter_by_language(get_language()).filter(tags__name__in=tags)
    context = {
        'post_list': posts,
    }
    return render(request, 'glarus_blog/post_list.html', context)


def blog_detail(request, slug):
    # post = Post.objects.filter_by_language(get_language()).filter(slug=slug).first()
    language = 'en-us' # currently nothing is translated to german so we give then en

    post = Post.objects.translated(language, slug=slug).first()
    context = {
        'post': post,
    }
    return render(request, 'glarus_blog/post_detail.html', context)


def support(request):
    return render(request, 'support.html')


def supporters(request):
    context = {
        'supporters': Supporter.objects.order_by('name')
    }
    return render(request, 'supporters.html', context)
