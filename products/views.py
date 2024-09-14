from pyexpat.errors import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from products.models import *
from products.serializers import *


class ProductListView(APIView):
    @staticmethod
    def get(request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    @staticmethod
    def get(request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryListView(APIView):
    @staticmethod
    def get(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetailView(APIView):
    @staticmethod
    def get(request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileListView(APIView):
    @staticmethod
    def get(request, product_pk):
        try:
            files = File.objects.filter(products__pk=product_pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileDetailView(APIView):
    @staticmethod
    def get(request, product_pk, pk):
        try:
            file = File.objects.get(pk=pk, products__id=product_pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(file, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
