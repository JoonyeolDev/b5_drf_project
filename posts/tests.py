from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
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


class PostingCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.posting_data = {"title": "test Title", "content": "test content"}
        cls.user = User.objects.create_user("test@test.com", "test", "Test1234!")

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    def test_create_posting_success(self):
        response = self.client.post(
            path=reverse("posting_view"),
            data=self.posting_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Posting.objects.count(), 1)
        self.assertEqual(Posting.objects.get().title, "test Title")

