from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from faker import Faker
from products.models import Product
from products.serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer, ProductReviewSerializer, ProductReviewCreateSerializer

# 이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file,'png')
    return


class ProductReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.products = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(),cls.faker.name(),cls.faker.password())
            cls.products.append(Product.objects.create(name=cls.faker.sentence(), introdution=cls.faker.text()))

    def test_get_product(self):
        for product in self.products:
            url = product.get_absolute_url()
            response = self.client.get(url)
            serializer = ProductSerializer(product).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)
