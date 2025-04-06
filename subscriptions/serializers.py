from rest_framework import serializers

from .models import Package, Subscription


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["title", "sku", "description", "avatar", "price", "duration"]


class SubscriptionSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True, read_only=True)
    class Meta:
        model = Subscription
        fields = ["packages", "created_time", "expire_time"]