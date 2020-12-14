from django.contrib import admin

from app.models import Mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    pass
