from django.contrib import admin
from django.urls import path, include

from mails.forms import SendMailForm
from mails.views import SendView, success_send
from mails.api import MailTemplateDetail, MailTemplateList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send_mail/', SendView.as_view(form_class=SendMailForm, success_url='/success_send/')),
    path('success_send/', success_send),
    path('api/mail/template/', MailTemplateList.as_view()),
    path('api/mail/template/<str:name>/', MailTemplateDetail.as_view()),
]
