import threading
import sys
from datetime import datetime

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail


THREADS = []


class Mail(models.Model):
    message = models.TextField(verbose_name='Message')
    from_address = models.EmailField(verbose_name='From email', max_length=155,
                                    default='gctdljgkjnm@mail.ru')
    to_address = models.EmailField(verbose_name='To email', max_length=155)
    WAITING = 'waiting to send'
    SENDED = 'sended'
    MAIL_STATUS = [
        (WAITING, 'Waiting to send'),
        (SENDED, 'Sended')
    ]
    status = models.CharField(max_length=15, choices=MAIL_STATUS, default=WAITING)
    creation_date = models.DateTimeField(auto_now_add=True)
    send_date = models.DateTimeField(default=None, blank=True, null=True)
    send_timeout = models.IntegerField(default=0)

    def __str__(self):
        return f'Status: {self.status} (from {self.from_address} to {self.to_address})'


# Sending email with a signal
def update_mail_data(mail_obj):
    """
    When email has sended updating the fields send_date and status.
    """
    date = datetime.now()
    Mail.objects.filter(pk=mail_obj.pk).update(send_date=date, status='sended')
    print('Send date updated.')


def send_mail_with_data(instance):
    """
    Sending email with a new data from the mail_obj.
    """
    try:
        send_mail(
            f'Message from {instance.from_address}',
            instance.message,
            instance.from_address,
            [instance.to_address],
            fail_silently=False,
        )
        print(f'Email has been sended. Timeout: {instance.send_timeout}')
        update_mail_data(instance)
    except:
        e = sys.exc_info()
        print(f'Sending error: {e}')


def add_thread(instance, **kwargs):
    """
    Adding the new thread with timeout.
    """
    timer = float(instance.send_timeout)
    t = threading.Timer(timer, send_mail_with_data, args=(instance,))
    t.start()


post_save.connect(add_thread, sender=Mail)

