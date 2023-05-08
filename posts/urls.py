from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostingView.as_view(), name="posting-list"),
    path("<int:posting_id>/", views.PostingDetailView.as_view(), name="posting-detail"),
]
