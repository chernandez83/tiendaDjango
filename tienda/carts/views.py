from django.shortcuts import render, redirect

from products.models import Product

from .models import Cart
from .utils import get_or_create_cart

def cart(request):
    # Crear una sesión
    # request.session['cart_id'] = '123'
    
    # Obtener sesión
    # session = request.session.get('cart_id')
    # print(f'session: {session}')
    
    # Eliminar sesión
    # request.session['cart_id'] = None
    cart = get_or_create_cart(request)
    
    return render(request, 'carts/cart.html', {
        'cart': cart,
    })

def add(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))
    cart.products.add(product)
    return render(request, 'carts/add.html', {
        'product': product,
    })
    
def remove(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))
    cart.products.remove(product)
    return redirect('carts:cart')