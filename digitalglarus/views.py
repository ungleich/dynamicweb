import datetime

from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import get_language
from djangocms_blog.models import Post

from .models import Message

class MessageForm(ModelForm):
    required_css_class = 'form-control'
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone_number', 'message' ]


def detail(request, message_id):
    p = get_object_or_404(Message, pk=message_id)

    context = { 'message': p, }
    return render(request, 'digitalglarus/detail.html', context)

def about(request):
    return render(request, 'digitalglarus/about.html')

def index(request):
    return render(request, 'digitalglarus/index.html')

def contact(request):
    message = Message(received_date=datetime.datetime.now())
    form = MessageForm(request.POST, instance=message)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("digitalglarus:contact"))

    # form = MessageForm()

    context = { 
        'form': form,
    }

    return render(request, 'digitalglarus/contact.html', context)


def blog(request):
    tags = ["glarus"]
    posts = Post.objects.filter(tags__name__in=tags)
    context = {
        'post_list': posts,
    }
    return render(request, 'glarus_blog/post_list.html', context)


def blog_detail(request, slug):
    language = get_language()
    post = Post.objects.translated(language, slug=slug).language(language).get()
    context = {
        'post': post,
    }
    return render(request, 'glarus_blog/post_detail.html', context)
