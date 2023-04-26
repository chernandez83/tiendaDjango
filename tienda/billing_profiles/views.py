from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from .models import BillingProfile

@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        if request.POST.get('stripeToken'):
            if not request.user.has_customer():
                request.user.create_customer_id()
                
            stripe_token = request.POST['stripeToken']
            billing_profile = BillingProfile.objects.create_by_stripe_token(request.user, stripe_token)
            
            if billing_profile:
                messages.success(request, 'Tarjeta creada exitosamente.')
    
    return render(request, 'billing_profiles/add.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })