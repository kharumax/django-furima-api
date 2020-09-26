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
    path('products/create/',ProductCreateView.as_view(),name="product_create"),
    path('products/<int:pk>/update/',ProductUpdateView.as_view(),name="product_update"),
    path('products/<int:pk>/delete/',ProductDeleteView.as_view(),name="product_delete"),

    # Order
    path('products/<int:pk>/order/',OrderCreateView.as_view(),name="product_order"),

    # MyPage
    path('mypage/',MyPageView.as_view(),name="mypage"),
    path('get_current_user/',GetCurrentUserView.as_view(),name="get_current_user"),
    
]