from django.urls import path

from . import views

app_name = 'billing_profiles'

urlpatterns = [
    path('add', views.add, name='add'),
]
