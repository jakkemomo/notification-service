import pika
from django import forms
from jinja2 import Template

from admin_panel.mails.models import MailTemplate


class SendMailForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    viewed_films_in_month = forms.IntegerField()
    month_params = forms.ChoiceField()
    genre_params = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["month_params"].choices = [
            (r.id, r) for r in MonthlyParams.objects.all()
        ]
        self.fields["genre_params"].choices = [
            (r.id, r) for r in GenresParams.objects.all()
        ]

    def process_action(self, action):
        if not self.is_valid():
            return
        mmp = MonthlyParams.objects.get(id=self.data["month_params"][0])
        gp = GenresParams.objects.get(id=self.data["genre_params"][0])
        template = MailTemplate.objects.get(name="monthly").body
        t = Template(template)
        t.render(username=self.data["username"])
        data = t.render(
            username=self.data["username"],
            films_count=mmp.films_in_month,
            serials_count=mmp.serials_in_month,
            month=mmp.month,
            viewed_films=self.data["viewed_films_in_month"],
            genre_viewed_films=gp.viewed_genre_films,
            preferred_genre=gp.preferred_genre,
            text=gp.text,
        )
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="hello")
        channel.basic_publish(
            exchange="", routing_key="hello", body=data.encode("utf-8")
        )
        connection.close()
