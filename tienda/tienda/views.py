from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from users.models import User

from .forms import RegisterForm

from products.models import Product

def index(request):
    # return HttpResponse("<h1>¡Hola Mundo!</h1>")
    products = Product.objects.all().order_by('-id') # En orden descendente
    return render(request, 'index.html', {
        'title': 'Productos',
        'message': 'Listado de Productos',
        'products': products,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Login exitoso para {user.username}')
            
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next', 'index'))
            
            return redirect('index')
        else:
            messages.warning(request, 'Usuario o contraseña no validos')

    return render(request, 'users/login.html', {
        # contexto
    })


def logout_view(request):
    logout(request)
    messages.success(request, f'Cierre de sesión exitoso')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    # crear formulario con los datos de POST o vacío si no hay POST
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, f'{user.username} creado exitosamente.')
            return redirect('index')

    return render(request, 'users/register.html', {
        'form': form
    })
