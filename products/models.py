from django.db import models

class Product(models.Model):
    _id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name + ' ' + self.brand