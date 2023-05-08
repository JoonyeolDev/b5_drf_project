from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostingView.as_view(), name="posting-view"),
    path("<int:posting_id>/", views.PostingDetailView.as_view(), name="posting-detail-view"),
    path("<int:posting_id>/comment/", views.CommentCreateView.as_view(), name="comment-create-view"),
    path("<int:posting_id>/comment/<int:comment_id>/", views.CommentView.as_view(), name="comment-view"),
]
