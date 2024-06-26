# Generated by Django 3.1.1 on 2021-04-09 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mails", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GenresParams",
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
                ("viewed_genre_films", models.IntegerField()),
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
                "verbose_name": "Жанр и текст о нём",
            },
        ),
        migrations.CreateModel(
            name="MonthlyParams",
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
                        choices=[
                            ("January", "январе"),
                            ("February", "феврале"),
                            ("March", "марте"),
                            ("April", "апреле"),
                        ],
                        default="April",
                        max_length=8,
                    ),
                ),
                ("films_in_month", models.IntegerField()),
                (
                    "serials_in_month",
                    models.CharField(
                        choices=[("horror", "хоррор"), ("tv_show", "шоу")],
                        max_length=16,
                    ),
                ),
            ],
            options={
                "verbose_name": "Новые фильмы в месяце",
            },
        ),
        migrations.DeleteModel(
            name="MonthlyMailingParams",
        ),
    ]
