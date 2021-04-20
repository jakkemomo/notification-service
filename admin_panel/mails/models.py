from django.db import models
from django.utils.translation import gettext_lazy as _
from jinja2 import Environment, TemplateSyntaxError


class MailTemplate(models.Model):
    name = models.CharField(max_length=50, unique=True)
    body = models.TextField()
    subject = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Email Template")
        verbose_name_plural = _("Email Templates")
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        """
        String representation of Template.
        :return: Name
        """
        return self.name

    def save(self, *args, **kwargs):
        body = self.body
        env = Environment(autoescape=True)
        try:
            env.parse(body)
        except TemplateSyntaxError:
            return None
        super(MailTemplate, self).save()
