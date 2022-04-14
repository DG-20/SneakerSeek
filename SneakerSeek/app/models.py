from django.db import models


class Shoe(models.Model):
    brand = models.CharField(max_length=100)
    collection = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    shoe_type = models.CharField(max_length=50)
    price = models.FloatField()
    gender = models.CharField(max_length=10)
    year_manufactured = models.PositiveIntegerField()
    condition = models.CharField(max_length=100)
    quadrant = models.CharField(max_length=2)
    seller = models.CharField(max_length=100)
    image_url = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
