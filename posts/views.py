from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Posting
from posts.serializers import PostingSerializer, PostingDetailSerializer

# Create your views here.


# posting/
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
    게시글 작성기능(모달창 사용?)
    title, content, image(선택)
    """

    def post(self, request):
        serializer = PostingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


# posting/<int:posting_id>/
class PostingDetailView(APIView):
    """
    게시글 상세보기 페이지
    id = posting_id인 게시글 1개 가져오기,
    (댓글 추가시) 댓글 fk가 posting_id인 댓글들도 가져오기
    """

    def get(self, request, posting_id):
        posting = get_object_or_404(Posting, id=posting_id)
        serializer = PostingDetailSerializer(posting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 수정하기
    posting.user == request.user인지 확인
    get요청으로 받아온 값들 default로 채워주기
    """

    def put(self, request, posting_id):
        # posting = get_object_or_404(Posting, id=posting_id)
        # if posting.user == request.user
        serializer = PostingDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        # return Response(status=status.HTTP_401_UNAUTHORIZED)
