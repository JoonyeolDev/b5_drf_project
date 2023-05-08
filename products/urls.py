from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name='product_list'),
    path("<int:product_id>/", views.ProductDetailView.as_view(), name='product_detail'),
]