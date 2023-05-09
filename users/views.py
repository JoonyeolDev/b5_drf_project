from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.models import User
from posts.serializers import PostingSerializer
from posts.models import Posting


from users.serializers import UserSerializer, UserUpdateSerializer, UserProfileSerializer


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
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("언팔로우했습니다.", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("팔로우했습니다.", status=status.HTTP_200_OK)


class MypageView(APIView):

    def get(self, request):
        postings = Posting.objects.filter(user=request.user).order_by('-created_at')
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
