from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id","email","password","username","profile_image","introduction","created_at","updated_at",
            "no_of_product","no_of_order","no_of_sold"
        ]
        extra_kwargs = {
            "password": {"write_only": True,"min_length": 5},
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(UserSerializer):

    class Meta:
        model = User
        fields = [
            "username","profile_image","introduction"
        ]
        extra_kwargs = {
            "password": {"write_only": True,"min_length": 5},
        }


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id","title","description","product_image","provider",
            "category","is_sold","created_at","price","provider_name","category_name"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "provider": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class Order(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "id","buyer","product","created_at"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "buyer": {"read_only": True},
            "product": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

