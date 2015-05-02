from django.shortcuts import render

from django.shortcuts import render


from .models import Message


def send_message(request):
    pass

def index(request):
    message_list = Message.objects.order_by('-received_date')[:5]
    context = { 'message_list': message_list, }
    return render(request, 'digital_glarus/index.html', context)
