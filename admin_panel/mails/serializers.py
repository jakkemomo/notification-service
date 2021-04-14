from .models import MailTemplate
from rest_framework import serializers
from jinja2 import Environment, TemplateSyntaxError


class MailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTemplate
        fields = ['name', 'body', 'subject']

    def is_valid(self, raise_exception=False):
        super(MailTemplateSerializer, self).is_valid()
        env = Environment()
        try:
            env.parse(self.initial_data['body'])
            return True
        except TemplateSyntaxError as e:
            raise e