from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostingView.as_view(), name="posting_view"),
    path("<int:posting_id>/", views.PostingDetailView.as_view(), name="posting_detail_view"),
    path("<int:posting_id>/comment/", views.CommentView.as_view(), name="comment_view"),
    path("<int:posting_id>/comment/<int:comment_id>/", views.CommentModifyView.as_view(), name="comment_modify_view"),
    path("<int:posting_id>/like/", views.LikeView.as_view(), name="like_view"),
]
