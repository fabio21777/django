from django.db import models

# Create your models here.
from django.db import models


class Question(models.Model):
    question_text = models.CharField("Descrição da questão",max_length=200)
    pub_date = models.DateTimeField("data de publicação")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
