from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from products.models import Product, ProductReview
from products.serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer, ProductReviewSerializer, ProductReviewCreateSerializer
from drf_project.permissions import IsAdminUserOrReadonly, IsAuthorOrReadonly
# Create your views here.

# product/
class ProductView(APIView):
    # IsAuthenticatedOrReadOnly : 인증된 사람은 쓰기 가능, 그 외 읽기만 가능[GET, HEAD, OPTIONS]
    # IsAdminUser : 관리자만 쓰기 가능[POST, PUT, PATCH, DELETE]
    permission_classes = [IsAdminUserOrReadonly]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# product/<int:product_id>/
class ProductDetailView(APIView):
    permission_classes = [IsAdminUserOrReadonly]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductCreateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"massage":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)


# product/<int:product_id>/review/
class ProductReviewView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = product.productreview_set.all()
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request, product_id):
        serializer = ProductReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# product/<int:product_id>/review/<int:review_id>
class ProductReviewDetailView(APIView):
    permission_classes = [IsAuthorOrReadonly]

    def get_object(self):
        obj = get_object_or_404(ProductReview, id=self.kwargs["review_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, product_id, review_id):
        review = get_object_or_404(ProductReview, id=review_id)
        serializer = ProductReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request, product_id, review_id):
        review = self.get_object()
        serializer = ProductReviewCreateSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, product_id, review_id):
        review = self.get_object()
        if request.user==review.user:
            review.delete()
            return Response({"massage":"삭제 완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"massage":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)


# product/<int:product_id>/like/
class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request, product_id):
        product = get_object_or_404(Product, id = product_id)
        if request.user in product.likes.all():
            product.likes.remove(request.user)
            return Response({"massage":"좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            product.likes.add(request.user)
            return Response({"massage":"좋아요를 눌렀습니다"}, status=status.HTTP_200_OK)


# product/<int:product_id>/review/<int:review_id>/like/
class ProductReviewLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id, review_id):
        review = get_object_or_404(ProductReview, id = review_id)
        if request.user in review.likes.all():
            review.likes.remove(request.user)
            return Response({"massage":"좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            review.likes.add(request.user)
            return Response({"massage":"좋아요를 눌렀습니다"}, status=status.HTTP_200_OK)