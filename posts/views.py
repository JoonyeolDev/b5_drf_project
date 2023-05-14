import datetime
from django.shortcuts import render
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from posts.models import Posting, Comment, Like
from posts.serializers import (
    PostingListSerializer,
    PostingDetailSerializer,
    PostingCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)


# 페이지네이션
class PostingPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10000


# posting/
class PostingView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostingPagination()
    """
    게시글 리스트 모두 보여주기(작성 시간순으로 정렬)
    추후 페이지네이션, 
    작성일 기준 정렬(최신순), 
    총 좋아요 기준 정렬(인기순), 
    7일 내 좋아요 기준 정렬(HOT 게시글?) 추가
    로그인 안해도 볼 수 있게
    """

    def get(self, request):
        # period = {
        #     "day": datetime.now() - datetime.timedelta(days=1),
        #     "week": datetime.now() - datetime.timedelta(days=7),
        #     "month": datetime.now() - datetime.timedelta(days=30),
        # }

        sort_get = request.GET.get("sort", "recent")
        # period_get = period.get(request.GET.get("period", "week"), "week")

        # like_queryset = Like.objects.filter(created_at__gte=start_date)
        # comment_queryset = Comment.objects.filter(created_at__gte=start_date)

        recent_posting = Posting.objects.all().order_by("-created_at")
        like_count_posting = Posting.objects.annotate(num_likes=Count("like")).order_by(
            "-num_likes"
        )
        comment_count_posting = Posting.objects.annotate(
            num_comments=Count("comment")
        ).order_by("-num_comments")
        if sort_get == "comment":
            query_set = comment_count_posting
        elif sort_get == "like":
            query_set = like_count_posting
        else:
            query_set = recent_posting

        page = self.pagination_class.paginate_queryset(query_set, request)
        serializer = PostingListSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    """
    게시글 작성기능
    title, content, image(선택)
    """

    def post(self, request):
        serializer = PostingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# posting/<int:posting_id>/
class PostingDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    게시글 상세보기 페이지
    id = posting_id인 게시글 1개 가져오기
    """

    def get(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        serializer = PostingDetailSerializer(posting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 수정하기
    posting.user == request.user인지 확인
    get요청으로 받아온 값들 default로 채워주기(프론트에서?)
    """

    def put(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        serializer = PostingDetailSerializer(posting, data=request.data)
        if posting.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    """
    게시글 삭제하기
    posting.user == request.user인지 확인
    """

    def delete(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        if posting.user == request.user:
            posting.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    댓글 보기
    posting_id가 일치하는 comment를 related_name으로 가져오기
    """

    def get(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        comments = posting.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    댓글 작성
    """

    def post(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posting=posting, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentModifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    댓글 수정
    """

    def put(self, request, posting_id, comment_id):
        posting = get_object_or_404(Posting, id=posting_id)
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if comment.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user, posting=posting)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    """
    댓글 삭제
    """

    def delete(self, request, posting_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    게시글 좋아요
    """

    def post(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        try:
            like = Like.objects.get(posting=posting, user=request.user)
            like.delete()
            like_count = posting.like_set.count()
            return Response({'liked': False, 'like_count': like_count}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            like = Like.objects.create(posting=posting, user=request.user)
            like_count = posting.like_set.count()
            return Response({'liked': True, 'like_count': like_count}, status=status.HTTP_200_OK)
