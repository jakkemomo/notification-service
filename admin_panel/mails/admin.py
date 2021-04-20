from django.contrib import admin

from admin_panel.mails.models import MailTemplate


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    pass
