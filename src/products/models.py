from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(max_length=9)

    tags = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )


class ProductMedia(models.Model):
    data = models.BinaryField(
        max_length=300*1024,
        null=False,
        blank=False
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='media'
    )


