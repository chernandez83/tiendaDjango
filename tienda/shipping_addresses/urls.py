from django.urls import path

from . import views

app_name = 'shipping_addresses'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_addresses'),
    path('new', views.new, name='new'),
    path('update/<int:pk>', views.ShippingAddressUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.ShippingAddressDeleteView.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default'),
]
