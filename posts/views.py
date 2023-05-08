from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Posting
from posts.serializers import PostingSerializer

# Create your views here.


class PostingView(APIView):
    """
    게시글 리스트 모두 보여주기(작성 시간순으로 정렬)
    추후 페이지네이션 추가
    """

    def get(self, request):
        posting_list = Posting.objects.all()
        serializer = PostingSerializer(posting_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 작성기능(모달창 사용시)
    """

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class PostingCreateView(APIView):
    """
    게시글 작성 페이지 띄워주기
    """

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    """
    게시글 작성 요청하기
    """

    def post(self, request):
        serializer = PostingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class PostingDetailView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        return Response(status=status.HTTP_200_OK)
