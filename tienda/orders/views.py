from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from shipping_addresses.models import ShippingAddress

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


@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    
    shipping_address = order.get_or_set_shipping_address()
    has_multiple_orders = request.user.shippingaddress_set.count() > 1
    
    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'breadcrumbs': breadcrumb(address=True),
        'shipping_address': shipping_address,
        'has_multiple_orders': has_multiple_orders,
    })

@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.all()
    
    return render(request, 'orders/select_address.html', {
        'breadcrumbs': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses,
    })

@login_required(login_url='login')
def check_address(request, pk):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)    
    
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    
    order.update_shipping_address(shipping_address)
    
    return redirect('orders:address')