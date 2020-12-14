import threading
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages

from app.models import Mail
from app.forms import MailForm, Mail1Form


class MailList(ListView):
    model = Mail
    template_name = 'pages/mail_list.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.order_by('-creation_date')[:10]

    def get_context_data(self, **kwargs):
        context = super(MailList, self).get_context_data(**kwargs)

        context['sended'] = Mail.objects.filter(status='sended')
        context['waiting_to_send'] = Mail.objects.filter(status='waiting to send')

        return context


class MailCreation(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('app:mail-list')
    template_name = 'pages/mail_create.html'


# Sendin email with a view
def update_mail_data(mail_obj):
    """
    Updating the fields send_date and status.
    """
    date = datetime.now()
    Mail.objects.filter(pk=mail_obj.pk).update(send_date=date, status='sended')
    print('Send date updated.')


def send_mail_with_data(mail_obj):
    """
    Sending email with a new data from the mail_obj.
    """
    send_mail(
        f'Message from {mail_obj.from_address}',
        mail_obj.message,
        mail_obj.from_address,
        [mail_obj.to_address],
        fail_silently=False
    )
    print(f'Email has been sended. Timeout: {mail_obj.send_timeout}')
    update_mail_data(mail_obj)


def add_thread(mail_obj):
    """
    Adding the new thread with timeout.
    """
    timer = float(mail_obj.send_timeout)
    t = threading.Timer(timer, send_mail_with_data, args=(mail_obj,))
    t.start()


def mail_creation(request):
    if request.method == 'POST':
        form = Mail1Form(request.POST)
        if form.is_valid:
            mail_to = request.POST.get('to_address')
            message = request.POST.get('message')
            timeout = request.POST.get('send_timeout')
            mail_obj = Mail.objects.create(message=message, to_address=mail_to, send_timeout=timeout)
            mail_obj.save()
            add_thread(mail_obj)
            return redirect(reverse_lazy('app:mail-list'))
        else:
            messages.error(request, 'Data error')
    else:
        form = Mail1Form()

    return render(request, 'pages/mail_create.html', {'form': form})
