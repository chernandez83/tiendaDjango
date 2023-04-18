from django.shortcuts import render
from django.views.generic import ListView

from .models import ShippingAddress
from .forms import ShippingAddressForm

class ShippingAddressListView(ListView):
    moderl = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'
    
    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

def new(request):
    form = ShippingAddressForm()
    return render(request, 'shipping_addresses/new.html', {
        'form': form,
    })