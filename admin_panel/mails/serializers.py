from rest_framework import serializers

from .models import MailTemplate


class MailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTemplate
        fields = ["name", "body", "subject"]
