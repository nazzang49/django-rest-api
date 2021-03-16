from django.db import models

# test
class Member(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    age = models.IntegerField(default=0)

class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.CharField(max_length=200)
    long = models.CharField(max_length=200)