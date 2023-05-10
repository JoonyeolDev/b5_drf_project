from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from rest_framework import status
from posts.models import Posting, Comment, Like
from users.models import User
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

# from faker import Faker


"""
posting_view
posting_detail_view
comment_view
comment_modify_view
like_view
"""


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, "png")
    return temp_file


# view = PostingView, url name = "posting_view", method = get, post
class PostingViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = {"title": "test Title", "content": "test content"}
        cls.user = User.objects.create_user("test@test.com", "test", "Test1234!")

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 게시글 작성 성공
    def test_create_posting_success(self):
        response = self.client.post(
            path=reverse("posting_view"),
            data=self.posting_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posting.objects.count(), 1)
        self.assertEqual(Posting.objects.get().title, "test Title")

    # 포스팅 모두보기(아무것도 없을 때)
    def test_get_posting_list_empty(self):
        response = self.client.get(path=reverse("posting_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    # 포스팅 모두보기(게시글 5개)
    def test_posting_list(self):
        self.posting = []
        for _ in range(5):
            self.posting.append(
                Posting.objects.create(**self.posting_data, user=self.user)
            )
        response = self.client.get(
            path=reverse("posting_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)


# view = PostingDetailView, url name = "posting_view", method = get, put, delete
class PostingDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = [
            {"title": "test Title1", "content": "test content1"},
            {"title": "test Title2", "content": "test content2"},
            {"title": "test Title3", "content": "test content3"},
            {"title": "test Title4", "content": "test content4"},
            {"title": "test Title5", "content": "test content5"},
        ]
        cls.user = User.objects.create_user("test@test.com", "test", "Test1234!")
        cls.posting = []
        for i in range(5):
            cls.posting.append(
                Posting.objects.create(**cls.posting_data[i], user=cls.user)
            )

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 게시글 상세보기 성공
    def test_posting_detail_view(self):
        response = self.client.get(
            path=reverse("posting_detail_view", kwargs={"posting_id": 5}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "test content5")

    # 게시글 수정하기
    def test_posting_detail_update_view(self):
        response = self.client.put(
            path=reverse("posting_detail_view", kwargs={"posting_id": 5}),
            data={"title": "updated test Title", "content": "updated test content"},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Posting.objects.count(), 5)
        self.assertEqual(response.data["content"], "updated test content")

    # 게시글 삭제하기
    def test_posting_detail_delete_view(self):
        response = self.client.delete(
            path=reverse("posting_detail_view", kwargs={"posting_id": 5}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertEqual(Posting.objects.count(), 4)


class CommentViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = {"title": "test Title", "content": "test content"}
        cls.comment_data = {"content": "test content"}
        cls.user = User.objects.create_user("test@test.com", "test", "Test1234!")
        cls.posting = Posting.objects.create(**cls.posting_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 코멘트 작성 성공
    def test_create_posting_success(self):
        response = self.client.post(
            path=reverse("comment_view", kwargs={"posting_id": 1}),
            data=self.comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "test content")

    # 코멘트 리스트 모두보기(아무것도 없을 때)
    def test_comment_list_empty(self):
        response = self.client.get(
            path=reverse("comment_view", kwargs={"posting_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    # 코멘트 리스트 모두보기(5개)
    def test_comment_list(self):
        self.comments = []
        for _ in range(5):
            self.comments.append(
                Comment.objects.create(
                    **self.comment_data, posting=self.posting, user=self.user
                )
            )
        response = self.client.get(
            path=reverse("comment_view", kwargs={"posting_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]["content"], "test content")
