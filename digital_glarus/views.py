import datetime

from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Message


def detail(request, message_id):
    p = get_object_or_404(Message, pk=message_id)

    context = { 'message': p, }
    return render(request, 'digital_glarus/detail.html', context)

def send_message(request):
    pass

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone_number', 'message' ]

def index(request):
    if request.method == 'POST':
        message = Message(received_date=datetime.datetime.now())
        form = MessageForm(request.POST, instance=message)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("digital_glarus:index"))

    form = MessageForm()
    message_list = Message.objects.order_by('-received_date')[:5]

    context = { 
        'message_list': message_list, 
        'form': form,
    }

    return render(request, 'digital_glarus/index.html', context)
