from .models import MailTemplate
from .serializers import MailTemplateSerializer
from rest_framework import generics


class MailTemplateDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = MailTemplate.objects.all()
    serializer_class = MailTemplateSerializer
    lookup_field = 'name'


class MailTemplateList(generics.ListCreateAPIView):

    queryset = MailTemplate.objects.all()
    serializer_class = MailTemplateSerializer


