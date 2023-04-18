from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from carts.utils import get_or_create_cart
# from .models import Order
from .utils import get_or_create_order, breadcrumb

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart=cart, request=request)
    
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumbs': breadcrumb(),
    })
