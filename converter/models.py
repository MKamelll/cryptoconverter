from django.db import models


class Coin(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    price: models.CharField = models.CharField(max_length=100)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Currency(name: {self.name}, price: {self.price}, updated_at: {self.updated_at})"
