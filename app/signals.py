# import threading
# from datetime import datetime
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
#
# from app.models import Mail
#
#
# def update_mail_data(mail_obj):
#     """
#     When email has sended updating the fields send_date and status.
#     """
#     date = datetime.now()
#     Mail.objects.filter(pk=mail_obj.pk).update(send_date=date, status='sended')
#     print('Send date updated.')
#
#
# def send_mail_with_data(instance):
#     """
#     Sending email with a new data from the mail_obj.
#     """
#     send_mail(
#         f'Message from {instance.from_address}',
#         instance.message,
#         instance.from_address,
#         [instance.to_address],
#         fail_silently=False,
#     )
#     print(f'Email has been sended. Timeout: {instance.send_timeout}')
#     update_mail_data(instance)
#
#
# @receiver(post_save, sender=Mail)
# def add_thread(instance, **kwargs):
#     """
#     Adding the new thread with timeout.
#     """
#     timer = float(instance.send_timeout)
#     t = threading.Timer(timer, send_mail_with_data, args=(instance,))
#     t.start()