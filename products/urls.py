from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name='product_list'),
    path("<int:product_id>/", views.ProductDetailView.as_view(), name='product_detail'),
    path("<int:product_id>/review/", views.ProductReviewView.as_view(), name='product_review'),
    path("<int:product_id>/review/<int:review_id>", views.ProductReviewDetailView.as_view(), name='product_review_detail'),
]