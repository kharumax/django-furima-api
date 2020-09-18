from django.urls import path,include
from .views import *

app_name = 'furima'

urlpatterns = [
    # User
    path('signup/',UserSignUpView.as_view(),name="signup"),
    path('users/<int:pk>/',UserRetrieveView.as_view(),name="user_retrieve"),
    path('users/',UserListView.as_view(),name="user_list"),
    path('user/<int:pk>/update/',UserUpdateView.as_view(),name="user_update"),
    # Product
    path('products/',ProductListView.as_view(),name="product_list"),
    path('products/<int:pk>/',ProductRetrieveView.as_view(),name="product_retrieve"),
    path('products/create/',ProductCreateView.as_view(),name="product_create")

    # Order
]