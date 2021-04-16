# Generated by Django 3.1.1 on 2021-04-08 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MailTemplate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("body", models.TextField()),
                ("subject", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Шаблон письма",
                "verbose_name_plural": "Шаблоны писем",
            },
        ),
        migrations.CreateModel(
            name="MonthlyMailingParams",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        choices=[("January", "январе"), ("February", "февраля")],
                        default="April",
                        max_length=8,
                    ),
                ),
                ("viewed_films", models.IntegerField()),
                (
                    "preferred_genre",
                    models.CharField(
                        choices=[("horror", "хоррор"), ("tv_show", "шоу")],
                        max_length=16,
                    ),
                ),
                ("text", models.TextField()),
            ],
            options={
                "verbose_name": "Данные для ежемесячного шаблона",
            },
        ),
        migrations.AddIndex(
            model_name="mailtemplate",
            index=models.Index(fields=["name"], name="mails_mailt_name_46717c_idx"),
        ),
    ]