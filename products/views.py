from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product, ProductReview
from products.serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer, ProductReviewSerializer, ProductReviewCreateSerializer

# Create your views here.

class ProductView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        # if not request.user.is_authenticated:
        #     return Response({"message":"로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        # if not request.user.is_superuser:
        #     return Response({"massage":"관리자 계정이 아닙니다"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ProductCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProductDetailView(APIView):
    def get(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        # if not request.user.is_superuser:
        #     return Response({"massage":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductCreateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        # if not request.user.is_superuser:
        #     return Response({"massage":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        return Response({"massage":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
    
class ProductReviewView(APIView):
    def get(self,request, product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = product.productreview_set.all()
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self,request, product_id):
        # if not request.user.is_authenticated:
        #     return Response({"message":"로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        # if not request.user.is_superuser:
        #     return Response({"massage":"관리자 계정이 아닙니다"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ProductReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewDetailView(APIView):
    def get(self,request, product_id):
        review = get_object_or_404(ProductReview, id=product_id)
        serializer = ProductReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request, product_id, review_id):
        product = get_object_or_404(Product, id=review_id)
        if not request.user.is_authenticated:
            serializer = ProductReviewSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

    def delete(self,request, product_id, review_id):
        product = get_object_or_404(Product, id=review_id)
        if not request.user.is_authenticated:
            product.delete()
            return Response("삭제 완료",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

class LikeView(APIView):
    def post(self,request, product_id):
        product = get_object_or_404(Product, id = product_id)
        if request.user in product.likes.all():
            product.likes.remove(request.user)
            return Response("좋아요를 취소했습니다", status=status.HTTP_200_OK)
        else:
            product.likes.add(request.user)
            return Response("좋아요를 눌렀습니다", status=status.HTTP_200_OK)

class ProductReviewLikeView(APIView):
    def post(self,request, review_id):
        review = get_object_or_404(ProductReview, id = review_id)
        if request.user in review.likes.all():
            review.likes.remove(request.user)
            return Response("좋아요를 취소했습니다", status=status.HTTP_200_OK)
        else:
            review.likes.add(request.user)
            return Response("좋아요를 눌렀습니다", status=status.HTTP_200_OK)