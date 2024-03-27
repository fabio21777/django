from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

STATUS_CHOICES = {
    "d": "Draft",
    "p": "Published",
    "w": "Withdrawn",
}

class Question(models.Model):
    question_text = models.CharField("Descrição da questão",max_length=200)
    pub_date = models.DateTimeField("data de publicação")
    status = models.CharField("Publicada",max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name="Questão")
    choice_text = models.CharField("Descrição da Questão",max_length=200)
    votes = models.IntegerField("Votos",default=0)

    def __str__(self):
        return self.choice_text
