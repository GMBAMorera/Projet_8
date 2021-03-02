from django.db import models
from login.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)


class Aliment(models.Model):
    name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    ingredients = models.TextField()
    cat_name = models.ForeignKey(Category, on_delete=models.CASCADE)

class Substitution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    substitute = models.ForeignKey(Aliment, on_delete=models.CASCADE, related_name='aliment_substitute')
    original = models.ForeignKey(Aliment, on_delete=models.CASCADE, related_name='aliment_original')