from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Posting, Comment
from posts.serializers import (
    PostingSerializer,
    PostingDetailSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)

# Create your views here.


# posting/
class PostingView(APIView):
    """
    게시글 리스트 모두 보여주기(작성 시간순으로 정렬)
    추후 페이지네이션 추가
    로그인 안해도 볼 수 있게?
    """

    def get(self, request):
        posting_list = Posting.objects.all()
        serializer = PostingSerializer(posting_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 작성기능(모달창 사용?)
    title, content, image(선택)
    """

    def post(self, request):
        serializer = PostingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


# posting/<int:posting_id>/
class PostingDetailView(APIView):
    """
    게시글 상세보기 페이지
    id = posting_id인 게시글 1개 가져오기,
    (댓글 추가시) 댓글 fk가 posting_id인 댓글들도 가져오기
    """

    def get(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        comment = Comment.objects.filter(id=posting_id)
        serializer = PostingDetailSerializer(posting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 수정하기
    posting.user == request.user인지 확인
    get요청으로 받아온 값들 default로 채워주기
    """

    def put(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        serializer = PostingDetailSerializer(posting, data=request.data)
        # if posting.user == request.user
        if serializer.is_valid():
            serializer.save()
            # serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #   return Response(status=status.HTTP_401_UNAUTHORIZED)

    """
    게시글 삭제하기
    posting.user == request.user인지 확인
    """

    def delete(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        # if posting.user == request.user
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        #   return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentView(APIView):
    """
    댓글 보기
    posting.user == request.user인지 확인
    """

    def get(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        comments = posting.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, posting_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posting_id=posting_id)
            # serializer.save(posting_id=posting_id, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentModifyView(APIView):
    def put(self, request, posting_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(posting_id=posting_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # serializer.save(user=request.user, posting=posting)

    def delete(self, request, posting_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        # if comment.user == request.user:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        # return Response(status=status.HTTP_400_BAD_REQUEST)
