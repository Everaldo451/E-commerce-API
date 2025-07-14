from django.db import models
from backend.core.enums import OrderStatus
from products.models import Product
from users.models import User

class Order(models.Model):
    products = models.ManyToManyField(
        Product,
        related_name='+'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=[(status.value, status.name.title()) for status in OrderStatus],
        default=OrderStatus.PENDING.value,
    )
