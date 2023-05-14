from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('mock/', views.MockView.as_view(), name='mock_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.UserView.as_view(), name="user_view"),
    path('profile/', views.ProfileView.as_view(), name="myprofile_view"),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"),
    path('follow/', views.FollowView.as_view(), name="myfollow_view"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name="follow_view"),
    path('mypage/<int:user_id>/', views.MypageView.as_view(), name="mypage_view"),
    path('myfeed/', views.MyfeedFollowView.as_view(), name="myfeed_follow_view"),
    path('myfeed/like/', views.MyfeedLikeView.as_view(), name="myfeed_like_view"),
]