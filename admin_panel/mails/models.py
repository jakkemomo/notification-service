from django.db import models
from django.utils.translation import gettext_lazy as _
from jinja2 import Environment, TemplateSyntaxError


class MailTemplate(models.Model):
    name = models.CharField(max_length=50, unique=True)
    body = models.TextField()
    subject = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Шаблон письма')
        verbose_name_plural = _('Шаблоны писем')
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        body = self.body
        env = Environment()
        try:
            env.parse(body)
        except TemplateSyntaxError:
            return
        super(MailTemplate, self).save()


