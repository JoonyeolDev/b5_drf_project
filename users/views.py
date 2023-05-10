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


from users.serializers import (
    UserSerializer, 
    UserUpdateSerializer, 
    UserProfileSerializer,
    UserMypageSerializer,
    UserFeedSerializer
)


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "회원 탈퇴!"})

    def put(self, request):
        serializer = UserUpdateSerializer(
            instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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
    
    def get(self, request):
        pass


# user/mypage/<int:user_id>/
class MypageView(APIView):

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# user/mypage/like/
class MyfeedLikeView(APIView):    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        me = request.user
        serializer = UserFeedSerializer(me)
        like_posting_ids = me.like_set.all().values_list("posting_id")

        q = Q()  # 아직 filter하지 않은 모든 것
        for like_posting_id in like_posting_ids:
            q.add(Q(id=like_posting_id[0]), q.OR)
        
        if len(q) == 0:  # 아직 좋아요 한 게시글이 없을 경우. Posting.objects.filter(q): 모든 게시글.
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            liked_postings = Posting.objects.filter(q)
            me_like_posting_serializer = PostingSerializer(liked_postings, many=True)
            return Response((
                serializer.data,  # 좋아요한 상품, 리뷰
                me_like_posting_serializer.data  # 좋아요한 게시글
                ), status=status.HTTP_200_OK)


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