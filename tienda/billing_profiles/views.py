from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required(login_url='login')
def add(request):
    return render(request, 'billing_profiles/add.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })