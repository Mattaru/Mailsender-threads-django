from django import forms

from app.models import Mail


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['to_address', 'message', 'send_timeout']


class Mail1Form(forms.Form):
    to_address = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())
    send_timeout = forms.IntegerField()