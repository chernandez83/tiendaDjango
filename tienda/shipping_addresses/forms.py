from django.forms import ModelForm

from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['line1', 'line2', 'city', 'state', 'country', 'zipcode', 'reference']
        labels = {
            'line1': 'Calle 1', 
            'line2': 'Calle 2', 
            'city': 'Ciudad', 
            'state': 'Estado', 
            'country': 'País', 
            'zipcode': 'Código Postal', 
            'reference': 'Referencias',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['line1'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['line2'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['state'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
        })
        
        self.fields['zipcode'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '00000',
        })
        
        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
        })