from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Posting
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


# class PostingCreateTest(APITestCase):
#     # 한번만 실행, 데이터베이스에 대한 모든 초기데이터 생성
#     # 모든 테스트에서 공통으로 사용될 데이터
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_data = {
#             "email": "test@testuser.com",
#             "password": "testpassword",
#             "username": "bbb",
#             "gender": "F",
#             "date_of_birth": "2001-01-01",
#         }
#         cls.posting_data = {
#             "title": "test title",
#             "content": "test content",
#         }
#         cls.user = User.objects.create_user("test@testuser.com", "testpassword")

#     # 각각 테스트 마다 실행되는 메소드
#     # 테스트에 필요한 데이터를 초기화 하거나 설정
#     def setUp(self):
#         self.access_token = self.client.post(
#             reverse("token_obtain_pair"), self.user_data
#         ).data["access"]

#     def test_fail_if_not_logged_in(self):
#         url = reverse("posting_view")
#         response = self.client.post(url, self.article_data)
#         self.assertEqual(response.status_code, 401)


class PostingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password",
            email="test@test.com",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_posting(self):
        url = reverse("posting_view")
        data = {"title": "Test Title", "content": "Test Content", "image": None}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posting.objects.count(), 1)
        self.assertEqual(Posting.objects.get().title, "Test Title")
