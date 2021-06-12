from django.db import models
from django.conf import settings


# Create your models here.

class Ice_Cream(models.Model):
    name = models.CharField(max_length=200)
    images = models.ImageField()
    price = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(default=0)
    ice_size = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    size = models.CharField(max_length=1, choices=ice_size)
    ice_categories = (
        ('N', 'Normal'),
        ('G', 'Good'),
        ('D', 'Delicious'),
    )
    categories = models.CharField(max_length=100, choices=ice_categories, default='')
    ice_frequency = (
        ('F', 'Favorite'),
        ('L', 'Little'),
    )
    frequencies = models.CharField(max_length=100, choices=ice_frequency, default='')
    description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return f"{self.name}"


class Comments(models.Model):
    post = models.ForeignKey(Ice_Cream, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Statistics(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(max_length=100, default=0)
    items = models.CharField(max_length=1000, default='')
    items_size = models.CharField(max_length=1000, default='')

    def __str__(self):
        return f"{self.customer}"