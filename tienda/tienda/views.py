from django.shortcuts import render, redirect
# from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import RegisterForm

def index(request):
    # return HttpResponse("<h1>¡Hola Mundo!</h1>")
    return render(request, 'index.html', {
        'title': 'Productos',
        'message': 'Listado de Productos',
        'products': [
            {'title': 'Playera', 'price': 5, 'stock': True},  # producto
            {'title': 'Camisa', 'price': 7, 'stock': True},
            {'title': 'Mochila', 'price': 20, 'stock': False},
            {'title': 'Laptop', 'price': 500, 'stock': True},
        ]
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Login exitoso para {user.username}')
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
    # form = RegisterForm({
    #     'username': 'batman',
    #     'email': 'batman@jl.com',
    # })
    
    # crear formulario con los datos de POST o vacío si no hay POST
    form = RegisterForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        # username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password')
        # # User.objects.create_user encripta el password
        # user = User.objects.create_user(username=username, email=email, password=password)
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, f'{user.username} creado exitosamente.')
            return redirect('index')
    
    return render(request, 'users/register.html', {
        'form': form
    })
