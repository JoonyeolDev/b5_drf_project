from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.models import User
from posts.models import Posting
from posts.serializers import PostingSerializer
from products.models import ProductReview
from products.serializers import ProductReviewSerializer
from django.db.models.query_utils import Q
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (
    UserSerializer, 
    UserUpdateSerializer, 
    UserProfileSerializer,
    UserMypageSerializer,
    UserFeedSerializer,
    UserFollowSerializer,
    CustomTokenObtainPairSerializer
)

# user/signup/
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response("mock: get 요청")


# user/profile/
class ProfileView(APIView):
    """
    회원 탈퇴
    is_active = False로 변경만 하고 회원 정보는 계속 보관
    email(아이디), name 남아있어서 탈퇴한 회원이 같은 정보로 재가입 불가
    """
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "회원 탈퇴!"})

    """
    프로필 정보 수정
    """
    def put(self, request):
        serializer = UserUpdateSerializer(
            instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """
    사용자 프로필 조회
    user_id로 아무나 프로필 조회 가능
    """
    # user/profile/<int:user_id>/
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    팔로우/언팔로우 요청
    """
    # user/follow/<int:user_id>/
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me.id == you.id:
            return Response("자기 자신은 팔로우할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        else:
            if me in you.followers.all():
                you.followers.remove(me)
                return Response("언팔로우했습니다.", status=status.HTTP_200_OK)
            else:
                you.followers.add(me)
                return Response("팔로우했습니다.", status=status.HTTP_200_OK)
    
    """
    내가 팔로우한 사람/나를 팔로우한 사람 보기
    """
    # user/follow/
    def get(self, request):
        user = request.user
        serializer = UserFollowSerializer(user)
        
        following_info_set = {}
        
        for i in serializer.data["followings"]:
            following = get_object_or_404(User, username=i)
            following_info_set[f"{following.username}"] = []
            
            following_info_set[f"{following.username}"].append(following.username)
            following_info_set[f"{following.username}"].append(following.email)
            following_info_set[f"{following.username}"].append(str(following.image))
            following_info_set[f"{following.username}"].append(following.id)
        
        follower_info_set = {}
        
        for i in serializer.data["followers"]:
            follower = get_object_or_404(User, username=i)
            follower_info_set[f"{follower.username}"] = []
            
            follower_info_set[f"{follower.username}"].append(follower.username)
            follower_info_set[f"{follower.username}"].append(follower.email)
            follower_info_set[f"{follower.username}"].append(str(follower.image))
            follower_info_set[f"{follower.username}"].append(follower.id)

        return Response((serializer.data, following_info_set, follower_info_set), status=status.HTTP_200_OK)

"""
특정 사용자가 작성한 게시글과 리뷰 보기
"""
# user/mypage/<int:user_id>/
class MypageView(APIView):

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
내가 좋아요한 상품, 리뷰, 게시글 보기
"""
# user/myfeed/like/
class MyfeedLikeView(APIView):    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        me = request.user
        serializer = UserFeedSerializer(me)
        like_posting_ids = me.like_set.all().values_list("posting_id")

        q = Q()
        for like_posting_id in like_posting_ids:
            q.add(Q(id=like_posting_id[0]), q.OR)
        
        if len(q) == 0:  # 아직 좋아요 한 게시글이 없을 경우. Posting.objects.filter(q): 모든 게시글.
            return Response(serializer.data, status=status.HTTP_200_OK)  # 좋아요한 상품, 리뷰 데이터만 보냄
        else:
            liked_postings = Posting.objects.filter(q)
            me_like_posting_serializer = PostingSerializer(liked_postings, many=True)
            return Response((
                serializer.data,  # 좋아요한 상품, 리뷰
                me_like_posting_serializer.data  # 좋아요한 게시글
                ), status=status.HTTP_200_OK)

"""
내가 팔로우 하는 사람이 작성한 게시글과 리뷰 보기
"""
# user/myfeed/
class MyfeedFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        
        me = request.user

        q = Q()

        for following in me.followings.all():
            q.add(Q(user=following), q.OR)
        
        if len(q) == 0:  # 아무도 팔로우하지 않았을 경우. Posting.objects.filter(q): 모든 게시글.
            return Response("팔로우한 사용자가 없습니다.", status=status.HTTP_200_OK)
        else:
            postings = Posting.objects.filter(q)
            posting_serializer = PostingSerializer(postings, many=True)
            reviews = ProductReview.objects.filter(q)
            review_serializer = ProductReviewSerializer(reviews, many=True)
            return Response((posting_serializer.data, review_serializer.data), status=status.HTTP_200_OK)
        