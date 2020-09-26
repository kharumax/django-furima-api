from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated,BasePermission
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
import json

User = get_user_model()


# User
class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            "success": True,
            "status": status_code,
            "message": "SignUp Completed!"
        }
        return Response(response,status=status_code)


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        user = User.objects.get(id=user_id)
        status_code = status.HTTP_200_OK
        if user.profile_image:
            image_url = user.profile_image.url
        else:
            image_url = ""
        response = {
            "success": True,
            "status": status_code,
            "data": {
                "username": user.username,
                "profile_image": image_url,
                "introduction": user.introduction
            }
        }
        return Response(response,status=status_code)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()


class UserUpdatePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,UserUpdatePermission)
    queryset = User.objects.all()


# Product
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        # キーワード検索を行う場合
        if "keyword" in self.request.GET and self.request.GET["keyword"] is not None:
            keyword = self.request.GET["keyword"]
            keywords = keyword.split(' ')
            for word in keywords:
                queryset = queryset.filter(
                    Q(title__icontains=word) | Q(description__icontains=word)
                )
        # カテゴリ検索を行う場合
        if "categories" in self.request.GET and self.request.GET["categories"] is not None:
            category_id = self.request.GET["categories"]
            queryset = queryset.filter(category=category_id)
        return queryset


class ProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("pk")
        product = Product.objects.get(id=product_id)
        if product.product_image:
            image_url = product.product_image.url
        else:
            image_url = ""
        response = {
            "success": True,
            "status": status.HTTP_200_OK,
            "data": {
                "title": product.title,
                "description": product.description,
                "image_url": image_url,
                "provider_name": product.provider.username,
                "category_name": product.category.name,
                "is_sold": product.is_sold,
                "price": product.price,
                "created_at": product.created_at,
            }
        }
        return Response(response,status=status.HTTP_200_OK)


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(provider=self.request.user)
        response = {
            "success": True,
            "status": status.HTTP_201_CREATED,
            "data": serializer.data
        }
        return Response(response,status=status.HTTP_201_CREATED)


class ProductPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.provider.id == request.user.id


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,ProductPermission)
    queryset = Product.objects.all()


class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, ProductPermission)
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs.get("pk"))
        if product.provider.id == self.request.user.id:
            product.delete()
        else:
            raise PermissionError
        response = {
            "success": True,
            "status": status.HTTP_204_NO_CONTENT
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)


# Order
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id=self.kwargs.get("pk"))
        serializer.save(buyer=self.request.user,product=product)
        response = {
            "success": True,
            "status": status.HTTP_201_CREATED,
            "data": serializer.data
        }
        return Response(response,status=status.HTTP_201_CREATED)


class MyPageView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = self.request.user
        products = Order.objects.filter(buyer=user).product
        json_products = json.dumps(products.to_dict())

        if user.profile_image:
            image_url = user.profile_image.url
        else:
            image_url = ""
        response = {
            "username": user.username,
            "profile_image": image_url,
            "introduction": user.introduction,
            "products": json_products
        }
        return Response(response,status=status.HTTP_200_OK)


class GetCurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = self.request.user
        if user.profile_image:
            image_url = user.profile_image.url
        else:
            image_url = ""
        response = {
            "username": user.username,
            "profile_image": image_url,
            "introduction": user.introduction
        }
        return Response(response,status=status.HTTP_200_OK)
