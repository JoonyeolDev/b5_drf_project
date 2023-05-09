from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.UserView.as_view(), name="user_view"),
    path('profile/', views.ProfileView.as_view(), name="profile_view"),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name="follow_view"),
    path('mypage/', views.MypageView.as_view(), name="mypage_view"),
]