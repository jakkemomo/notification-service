from django.contrib import admin
from django.urls import path
from admin_panel.mails.api import MailTemplateDetail, MailTemplateList

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/mail/template/", MailTemplateList.as_view()),
    path("api/mail/template/<str:name>/", MailTemplateDetail.as_view()),
]
