from django.db import models
from django.utils.translation import gettext_lazy as _
from jinja2 import Environment, TemplateSyntaxError

from datetime import datetime


class MailTemplate(models.Model):
    name = models.CharField(max_length=50, unique=True)
    body = models.TextField()
    subject = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Mail Template')
        verbose_name_plural = _('Mail Templates')
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


months = [
    ('January', _('январе')),
    ('February', _('феврале')),
    ('March', _('марте')),
    ('April', _('апреле')),
    ('May', _('мае')),
]


class Genres(models.TextChoices):
    HORROR = 'horror', _('хоррор')
    TV_SHOW = 'tv_show', _('шоу')


class GenresParams(models.Model):
    viewed_genre_films = models.PositiveIntegerField()
    preferred_genre = models.CharField(choices=Genres.choices, max_length=16)
    text = models.TextField()

    class Meta:
        verbose_name = _('Жанр и текст о нём')
        verbose_name_plural = _('Жанры и тексты')

    def __str__(self):
        return " ". join((str(self.viewed_genre_films), self.preferred_genre))


class MonthlyParams(models.Model):
    month = models.CharField(default=datetime.now().strftime('%B'), choices=months, max_length=8)
    films_in_month = models.IntegerField()
    serials_in_month = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Новые фильмы в месяце')

    def __str__(self):
        return " ". join((str(self.month), str(self.films_in_month)))


