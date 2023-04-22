from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shipping_addresses.models import ShippingAddress

from carts.utils import get_or_create_cart, destroy_cart
from .utils import get_or_create_order, breadcrumb, destroy_order

from .mails import Mail

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
    has_multiple_addresses = request.user.shippingaddress_set.count() > 1

    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'breadcrumbs': breadcrumb(address=True),
        'shipping_address': shipping_address,
        'has_multiple_addresses': has_multiple_addresses,
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


@login_required(login_url='login')
def confirm(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')

    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumbs': breadcrumb(address=True, confirmation=True),
    })


@login_required(login_url='login')
def cancel(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    destroy_cart(request)
    destroy_order(request)

    messages.warning(request, 'Orden cancelada')
    return redirect('index')

@login_required(login_url='login')
def complete(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    
    if request.user.id != order.user_id:
        return redirect('carts:cart')
    
    order.complete()
    Mail.send_complete_order(order, request.user)
    
    destroy_cart(request)
    destroy_order(request)
    
    messages.success(request, 'Compra completada exitosamente')
    return redirect('index')