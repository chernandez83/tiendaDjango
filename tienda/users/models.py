from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from orders.common import OrderStatus

class User(AbstractUser):
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()
    
    def has_shipping_address(self):
        return self.shipping_address is not None
    
    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')
    
    @property
    def has_multiple_addresses(self):
        return self.shippingaddress_set.exists()
    
    @property
    def addresses(self):
        return self.shippingaddress_set.all()

class Customer(User):
    class Meta:
        proxy = True  # Modelo no genera tabla en la BD

    def get_products(self):
        return []


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()


# AbstractUser ó AbstractBaseUser 
# AbstractUser
# username
# first_name
# last_name
# email
# password
# groups
# user_permissions
# is_staff
# is_active
# is_superuser
# last_login
# date_joined

# AbstractBaseUser
# id
# password
# last_login