from rest_framework import generics

from admin_panel.mails.models import MailTemplate
from admin_panel.mails.serializers import MailTemplateSerializer


class MailTemplateDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = MailTemplate.objects.all()
    serializer_class = MailTemplateSerializer
    lookup_field = "name"


class MailTemplateList(generics.ListCreateAPIView):

    queryset = MailTemplate.objects.all()
    serializer_class = MailTemplateSerializer
