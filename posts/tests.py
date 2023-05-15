from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from rest_framework import status
from posts.models import Posting, Comment, Like
from users.models import User
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile
import os

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
        cls.user = User.objects.create_user(
            "test@test.com", "test", "Test1234!")

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 테스트 후 이미지 파일 삭제하기
    def tearDown(self):
        for posting in Posting.objects.all():
            posting.image.delete()
            posting.delete()

    # 게시글 작성
    def test_create_posting_success(self):
        response = self.client.post(
            path=reverse("posting_view"),
            data=self.posting_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posting.objects.count(), 1)
        self.assertEqual(Posting.objects.get().title, "test Title")

    # 이미지가 있는 게시글 작성
    def test_create_posting_with_image(self):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.posting_data["image"] = image_file
        response = self.client.post(
            path=reverse("posting_view"),
            data=encode_multipart(data=self.posting_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posting.objects.count(), 1)
        self.assertEqual(Posting.objects.get().title, "test Title")
        # self.assertEqual(bool(Posting.objects.get().image), True)

    # 게시글 모두보기(아무것도 없을 때)
    def test_get_posting_list_empty(self):
        response = self.client.get(path=reverse("posting_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    # 게시글 모두보기(게시글 5개)
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
        self.assertEqual(len(response.data), 4)


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
        cls.user = User.objects.create_user(
            "test@test.com", "test", "Test1234!")
        cls.posting = []
        for i in range(5):
            cls.posting.append(
                Posting.objects.create(**cls.posting_data[i], user=cls.user)
            )

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 게시글 상세보기
    def test_posting_detail(self):
        response = self.client.get(
            path=reverse("posting_detail_view", kwargs={"posting_id": 5}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "test content5")

    # 게시글 수정하기
    def test_posting_detail_update(self):
        response = self.client.put(
            path=reverse("posting_detail_view", kwargs={"posting_id": 5}),
            data={"title": "updated test Title",
                  "content": "updated test content"},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Posting.objects.count(), 5)
        self.assertEqual(response.data["content"], "updated test content")

    # 게시글 삭제하기
    def test_posting_detail_delete(self):
        response = self.client.delete(
            path=reverse("posting_detail_view", kwargs={"posting_id": 5}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Posting.objects.count(), 4)
        self.assertEqual(response.data, None)


# view = CommentView, url name = "comment_view", method = get, post
class CommentViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = {"title": "test Title", "content": "test content"}
        cls.comment_data = {"content": "test content"}
        cls.user = User.objects.create_user(
            "test@test.com", "test", "Test1234!")
        cls.posting = Posting.objects.create(**cls.posting_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 코멘트 작성
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]["content"], "test content")


# view = CommentModifyView, url name = "comment_modify_view", method = put, delete
class CommentModifyViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = {"title": "test Title", "content": "test content"}
        cls.comment_data = [
            {"content": "test content1"},
            {"content": "test content2"},
            {"content": "test content3"},
            {"content": "test content4"},
            {"content": "test content5"},
        ]
        cls.user = User.objects.create_user(
            "test@test.com", "test", "Test1234!")
        cls.posting = Posting.objects.create(**cls.posting_data, user=cls.user)
        cls.comments = []
        for i in range(5):
            cls.comments.append(
                Comment.objects.create(
                    **cls.comment_data[i], posting=cls.posting, user=cls.user
                )
            )

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 코멘트 수정하기
    def test_comment_update(self):
        response = self.client.put(
            path=reverse(
                "comment_modify_view", kwargs={"posting_id": 1, "comment_id": 1}
            ),
            data={"content": "updated test content"},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(response.data["content"], "updated test content")

    # 코멘트 삭제하기
    def test_comment_delete(self):
        response = self.client.delete(
            path=reverse(
                "comment_modify_view", kwargs={"posting_id": 1, "comment_id": 1}
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 4)
        self.assertEqual(response.data, None)


# view = LikeView, url name = "like_view", method = post
class LikeViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = {"title": "test Title", "content": "test content"}
        cls.user = User.objects.create_user(
            "test@test.com", "test", "Test1234!")
        cls.posting = Posting.objects.create(**cls.posting_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 좋아요 누르기
    def test_like_posting(self):
        response = self.client.post(
            path=reverse("like_view", kwargs={"posting_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'liked': True, 'like_count': 1})

    # 좋아요 취소하기
    def test_cancel_like_posting(self):
        like = Like.objects.create(user=self.user, posting=self.posting)
        response = self.client.post(
            path=reverse("like_view", kwargs={"posting_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'liked': False, 'like_count': 0})
