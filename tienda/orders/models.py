from django.db import models
from django.db.models.signals import pre_save

from enum import Enum
import uuid

from users.models import User
from carts.models import Cart


class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'


choices = [(tag, tag.value) for tag in OrderStatus]


class Order(models.Model):
    order_id = models.CharField(max_length=100,
                                null=False,
                                blank=False,
                                unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,
                              choices=choices,
                              default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=5,
                                         max_digits=8,
                                         decimal_places=2)
    total = models.DecimalField(default=0,
                                max_digits=8,
                                decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.cart.total + self.shipping_total
    
    def update_total(self):
         self.total = self.get_total()
         self.save()

    def __str__(self):
        return f'{self.user.username} {self.order_id}'


def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_order_id, Order)
pre_save.connect(set_total, Order)
