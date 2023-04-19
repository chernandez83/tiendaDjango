from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Para vistas normales
from django.contrib.auth.mixins import LoginRequiredMixin # Para vistas basasas en clases
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .models import ShippingAddress
from .forms import ShippingAddressForm


class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    moderl = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')


class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Dirección actualizada exitosamente'

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')
    
    # Validar que el usuario sea dueño de la dirección
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        
        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')
    success_message = 'Dirección eliminada exitosamente'
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')
        
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def new(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # crea pero no guarda en la bd
        shipping_address = form.save(commit=False)

        shipping_address.user = request.user
        shipping_address.default = not request.user.has_shipping_address()

        shipping_address.save()

        messages.success(request, 'Dirección creada exitosamente')

        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/new.html', {
        'form': form,
    })


@login_required(login_url='login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)
    
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    
    if request.user.has_shipping_address():
        request.user.shipping_address.update_default(default=False)
        
    shipping_address.update_default(default=True)
    
    messages.success(request, 'Dirección principal actualizada exitosamente')
    
    return redirect('shipping_addresses:shipping_addresses')