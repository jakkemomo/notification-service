from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mails.api import MailTemplateDetail, MailTemplateList

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/mail/template/", MailTemplateList.as_view()),
    path("api/mail/template/<str:name>/", MailTemplateDetail.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
