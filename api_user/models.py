from django.db import models

# test api
class Member(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    age = models.IntegerField(default=0)

# test location
class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.CharField(max_length=200)
    long = models.CharField(max_length=200)

# cafe default info
class CafeV1(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    long = models.DecimalField(max_digits=10, decimal_places=7)