import string
import random

from django.contrib import admin
from django.db.models.signals import pre_save

from .models import PromoCode

class PromoCodeAdmin(admin.ModelAdmin):
    exclude = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)

def set_code(sender, instance, *args, **kwargs):
    if instance.code:
        return
    
    chars = string.ascii_uppercase + string.digits
    instance.code = ''.join(random.choices(chars, k=10))

pre_save.connect(set_code, sender=PromoCode)