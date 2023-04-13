from django.urls import path

from . import views

urlpatterns = [
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]
