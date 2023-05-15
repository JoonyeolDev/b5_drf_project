from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from faker import Faker
from products.models import Product, ProductReview
from products.serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer, ProductReviewSerializer, ProductReviewCreateSerializer

# 이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile, random

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file,'png')
    return temp_file




class ReviewDeleteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user = User.objects.create_user('test@naver.com','test_joonyeol','password')
        cls.user_data = {'email':'test@naver.com','password':'password'}
        cls.another_user = User.objects.create_user('another@naver.com','another_joonyeol','password')
        cls.another_user_data = {'email':'another@naver.com','password':'password'}
        cls.product = Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text())
        cls.review = ProductReview.objects.create(user=cls.user, product=cls.product, score=random.randint(1,5), content=cls.faker.text())
    
    def setUp(self):
        self.user_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        self.another_user_token = self.client.post(reverse('token_obtain_pair'), self.another_user_data).data['access']

    # 로그인 안한 유저가 DELETE 요청 시 401
    def test_fail_if_not_logged_in(self):
        url = reverse("product_review_detail", kwargs={"product_id": self.product.id,"review_id":self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    # 작성자가 아닌 유저가 DELETE 요청 시 403
    def test_fail_if_not_author(self):
        response = self.client.delete(
            path = reverse("product_review_detail", kwargs={"product_id": self.product.id,"review_id":self.review.id}),
            HTTP_AUTHORIZATION = f"Bearer {self.another_user_token}"
        )
        self.assertEqual(response.status_code, 403)

    # 작성자가 DELETE 요청 시 204
    def test_delete_review(self):
        response = self.client.delete(
            path = reverse("product_review_detail", kwargs={"product_id": self.product.id,"review_id":self.review.id}),
            HTTP_AUTHORIZATION = f"Bearer {self.user_token}"
        )
        self.assertEqual(response.status_code, 204)


class ReviewUpdateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user = User.objects.create_user('test@naver.com','test_joonyeol','password')
        cls.user_data = {'email':'test@naver.com','password':'password'}
        cls.another_user = User.objects.create_user('another@naver.com','another_joonyeol','password')
        cls.another_user_data = {'email':'another@naver.com','password':'password'}
        cls.product = Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text())
        cls.review = ProductReview.objects.create(user=cls.user, product=cls.product, score=random.randint(1,5), content=cls.faker.text())
        cls.review_data = {'user':cls.user, 'product':cls.product, 'score':3, 'content':'update test content'}
    
    def setUp(self):
        self.user_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        self.another_user_token = self.client.post(reverse('token_obtain_pair'), self.another_user_data).data['access']

    # 로그인 안한 유저가 PUT 요청 시 401
    def test_fail_if_not_logged_in(self):
        url = reverse("product_review_detail", kwargs={"product_id": self.product.id,"review_id":self.review.id})
        response = self.client.put(url, self.review_data)
        self.assertEqual(response.status_code, 401)

    # 작성자가 아닌 유저가 PUT 요청 시 403
    def test_fail_if_not_author(self):
        response = self.client.put(
            path = reverse("product_review_detail", kwargs={"product_id": self.product.id,"review_id":self.review.id}),
            data = self.review_data,
            HTTP_AUTHORIZATION = f"Bearer {self.another_user_token}"
        )
        self.assertEqual(response.status_code, 403)

    # 작성자가 PUT 요청 시 200
    def test_update_review(self):
        response = self.client.put(
            path = reverse("product_review_detail", kwargs={"product_id": self.product.id,"review_id":self.review.id}),
            data = self.review_data,
            HTTP_AUTHORIZATION = f"Bearer {self.user_token}"
        )
        self.assertEqual(response.status_code, 200)

        # review 정보가 수정됐는지 확인
        update_review = ProductReview.objects.create(user=self.user, product=self.product, score=3, content='update test content')
        serializer = ProductReviewCreateSerializer(update_review).data
        for key, value in serializer.items():
            self.assertEqual(response.data[key], value) 
    
class ReviewCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user = User.objects.create_user('test@naver.com','test_joonyeol','password')
        cls.user_data = {'email':'test@naver.com','password':'password'}
        cls.product = Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text())
        cls.review_data = {'user':cls.user, 'product':cls.product, 'score':random.randint(1,5), 'content':cls.faker.text()}

    def setUp(self):
        self.user_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        # self.another_user_token = self.client.post(reverse('token_obtain_pair'), self.another_user_data).data['access']

    # 로그인 없이 post 요청 시 401 확인
    def test_fail_if_not_logged_in(self):
        url = reverse("product_review", kwargs={"product_id":self.product.id})
        response = self.client.post(url,self.review_data)
        self.assertEqual(response.status_code, 401)
        
    # 로그인 유저가 post 요청 시 201 확인
    def test_create_review(self):
        response = self.client.post(
            path = reverse("product_review", kwargs={"product_id":self.product.id}),
            data = self.review_data,
            HTTP_AUTHORIZATION = f"Bearer {self.user_token}"
        )
        self.assertEqual(response.status_code, 201)


class ReviewReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.product = Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text())
        cls.reviews = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(),cls.faker.name(),cls.faker.word())
            cls.reviews.append(ProductReview.objects.create(user=cls.user, product=cls.product, score=random.randint(1,5), content=cls.faker.text()))

    # 랜덤 생성한 review의 response와 serializer의 값이 같은지 확인
    def test_get_review(self):
        for review in self.reviews:
            url = review.get_absolute_url(self.product.id)
            response = self.client.get(url)
            serializer = ProductReviewSerializer(review).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)


class ProductDeleteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('admin@naver.com','admin_joonyeol','password')
        cls.admin_data = {'email':'admin@naver.com','password':'password'}
        cls.user = User.objects.create_user('test@naver.com','test_joonyeol','password')
        cls.user_data = {'email':'test@naver.com','password':'password'}
        # Faker를 사용해서 랜덤 product를 만듦
        cls.faker = Faker()
        cls.product = Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text())

    # admin, user의 access token을 받아옴
    def setUp(self):
        self.admin_access_token = self.client.post(reverse('token_obtain_pair'), self.admin_data).data['access']
        self.user_access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    # 로그인 없이 delete 요청 보내면 401 확인
    def test_fail_if_not_logged_in(self):
        url = reverse("product_detail", kwargs={"product_id":self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    # 로그인해도 admin이 아닌 user가 delete 요청 보내면 403 확인
    def test_fail_if_not_admin(self):
        response = self.client.delete(
            path=reverse("product_detail", kwargs={"product_id":self.product.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            )
        self.assertEqual(response.status_code, 403)

    # admin이 delete요청 보내면 204 확인
    def test_update_product(self):
        response = self.client.delete(
            path=reverse("product_detail", kwargs={"product_id":self.product.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}",
            )
        self.assertEqual(response.status_code, 204)


class ProductUpdateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('admin@naver.com','admin_joonyeol','password')
        cls.admin_data = {'email':'admin@naver.com','password':'password'}
        cls.user = User.objects.create_user('test@naver.com','test_joonyeol','password')
        cls.user_data = {'email':'test@naver.com','password':'password'}
        cls.product_data = {'name':'product test name','introduction':'product test introduction','brand':'product test brand'}
        # Faker를 사용해서 랜덤 product를 만듦
        cls.faker = Faker()
        cls.product = Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text())

    # admin, user의 access token을 받아옴
    def setUp(self):
        self.admin_access_token = self.client.post(reverse('token_obtain_pair'), self.admin_data).data['access']
        self.user_access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    # 로그인 없이 put요청 보내면 401 확인
    def test_fail_if_not_logged_in(self):
        url = reverse("product_detail", kwargs={"product_id":self.product.id})
        response = self.client.put(url, self.product_data)
        self.assertEqual(response.status_code, 401)

    # 로그인해도 admin이 아닌 user가 put요청 보내면 403 확인
    def test_fail_if_not_admin(self):
        response = self.client.put(
            path=reverse("product_detail", kwargs={"product_id":self.product.id}),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            )
        self.assertEqual(response.status_code, 403)

    # admin이 put요청 보내면 200 확인
    def test_update_product(self):
        response = self.client.put(
            path=reverse("product_detail", kwargs={"product_id":self.product.id}),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}",
            )
        self.assertEqual(response.status_code, 200)

        # product 정보가 수정됐는지 확인
        for key, value in self.product_data.items():
            self.assertEqual(response.data[key], value)

class ProductCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('admin@naver.com','admin_joonyeol','password')
        cls.admin_data = {'email':'admin@naver.com','password':'password'}
        cls.user = User.objects.create_user('test@naver.com','test_joonyeol','password')
        cls.user_data = {'email':'test@naver.com','password':'password'}
        cls.product_data = {'name':'product test name','introduction':'product test introduction','brand':'product test brand'}

    # admin, user의 access token을 받아옴
    def setUp(self):
        self.admin_access_token = self.client.post(reverse('token_obtain_pair'), self.admin_data).data['access']
        self.user_access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
        
    # 로그인 없이 post요청 보내면 401 확인
    def test_fail_if_not_logged_in(self):
        url = reverse("product_list")
        response = self.client.post(url, self.product_data)
        self.assertEqual(response.status_code, 401)

    # 로그인해도 admin이 아닌 user가 post요청 보내면 403 확인
    def test_fail_if_not_admin(self):
        response = self.client.post(
            path=reverse("product_list"),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            )
        self.assertEqual(response.status_code, 403)

    # admin이면 product 생성 확인
    def test_create_product(self):
        response = self.client.post(
            path=reverse("product_list"),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}",
            )
        self.assertEqual(response.status_code, 201)

    # image 업로드 되는지 확인
    def test_create_product_with_image(self):
        # 임시 image 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.product_data["image"] = image_file

        # image response
        response = self.client.post(
            path=reverse("product_list"),
            data=encode_multipart(data = self.product_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}"
        )
        self.assertEqual(response.status_code, 201)


class ProductReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Faker를 사용해서 10개의 랜덤 product를 만듦
        cls.faker = Faker()
        cls.products = []
        for i in range(10):
            cls.products.append(Product.objects.create(name=cls.faker.sentence(), introduction=cls.faker.text()))

    # 랜덤 생성한 product의 response와 serializer의 값이 같은지 확인
    def test_get_product(self):
        for product in self.products:
            url = product.get_absolute_url()
            response = self.client.get(url)
            serializer = ProductSerializer(product).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)
