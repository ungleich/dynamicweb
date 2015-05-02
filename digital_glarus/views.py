from django.shortcuts import render

from django.shortcuts import get_object_or_404, render



from .models import Message


def detail(request):
    pass

def detail(request, message_id):
    p = get_object_or_404(Message, pk=message_id)

    context = { 'message': p, }
    return render(request, 'digital_glarus/detail.html', context)

def send_message(request):
    pass

def index(request):
    message_list = Message.objects.order_by('-received_date')[:5]
    context = { 'message_list': message_list, }
    return render(request, 'digital_glarus/index.html', context)
