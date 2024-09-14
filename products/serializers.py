from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from products.models import Category, Product, File


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'description',
            'avatar'
        ]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            'title',
            'file_type',
            'file'
        ]


class ProductSerializer(serializers.ModelSerializer):

    class CategoryNameSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['title']

    categories = CategoryNameSerializer(many=True)

    files = FileSerializer(many=True)

    # foo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'avatar',
            'categories',
            'files'
        ]

    # def get_foo(self, obj):
    #     return obj.foo





