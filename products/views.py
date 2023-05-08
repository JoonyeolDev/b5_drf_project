from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer, ProductListSerializer

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
        
        serializer = ProductSerializer(data=request.data)

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
        #     serializer = ProductSerializer(product, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"massage":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        # if not request.user.is_superuser:
        #     product.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        #     return Response({"massage":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        return Response({"massage":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)