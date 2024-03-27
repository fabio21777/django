from django.db import models


SHIRT_SIZES = {
    "S": "Small",
    "M": "Medium",
    "L": "Large",
}

# Create your models here.
class Person(models.Model):
    first_name = models.CharField("Primeiro nome",max_length=30)
    last_name = models.CharField("Sobrenome",max_length=30)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()


