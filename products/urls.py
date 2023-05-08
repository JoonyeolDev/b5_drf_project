from django.urls import path,include
import views

urlpatterns = [
    path("", views.ProductCreateView.as_view(), name='product_create'),
]