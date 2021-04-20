from jinja2 import Environment
from rest_framework import serializers

from .models import MailTemplate


class MailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTemplate
        fields = ["name", "body", "subject"]

    def is_valid(self, raise_exception=False):
        super(MailTemplateSerializer, self).is_valid()
        env = Environment(autoescape=True)
        env.parse(self.initial_data["body"])
        return True
