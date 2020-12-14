from django.urls import path

from app.views import MailList, MailCreation, mail_creation


app_name = 'app'

urlpatterns = [
    path('mails/', MailList.as_view(), name='mail-list'),
    path('mails/create/', MailCreation.as_view(), name='mail-create'),
    path('mails/create/1/', mail_creation, name='mail-create1')
]