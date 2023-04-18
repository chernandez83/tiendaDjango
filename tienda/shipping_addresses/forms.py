from django.forms import ModelForm

from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['line1', 'line2', 'city', 'state', 'country', 'zipcode', 'reference']