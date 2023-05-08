from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Posting

# Create your views here.


class PostingView(APIView):
    """
    게시글 리스트 모두 보여주기(작성 시간순으로 정렬)
    추후 페이지네이션 추가
    """
    def get(self, request):
        pass
    """
    게시글 작성기능(모달창 사용시)
    """
    def post(self, request):
        pass


class PostingCreateView(APIView):
    """
    게시글 작성 페이지 띄워주기
    """
    def get(self, request):
        pass
    """
    게시글 작성 요청하기
    """
    def post(self, request):
        pass


class PostingDetailView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass
    def put(self, request):
        pass
    def delete(self, request):
        pass
