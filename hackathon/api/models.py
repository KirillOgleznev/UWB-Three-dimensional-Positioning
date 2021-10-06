from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()


class Product(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateField()
    count_of_steps = models.IntegerField()
    speed = models.IntegerField()




