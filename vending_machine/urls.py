"""vending_machine URL Configuration
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from user_management.views import (
    UserCreateView, 
    UserListView, 
    UserListDetailView, 
    UserDeleteView,
    UserUpdateView,
    UserBuyerDepositView,
    UserResetDepositView,
    UserBuyerBuyView,
)
from vending_machine_management.views import(
    ProductCreateView,
    ProductListView,
    ProductListDetailView,
    ProductDeleteView,
    ProductUpdateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("schema/swagger-ui/", login_required(SpectacularSwaggerView.as_view(url_name="schema")), name="swagger-ui"),
    path('schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),

    path('user/', UserCreateView.as_view(), name='user-create'),
    path('users/', UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/', UserListDetailView.as_view(), name='user-list-detail'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),

    path('product/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductListDetailView.as_view(), name='product-list-detail'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),

    path('deposit/', UserBuyerDepositView.as_view(), name='user-deposit'),
    path('deposit/reset/', UserResetDepositView.as_view(), name='user-deposit-reset'),
    path('buy/', UserBuyerBuyView.as_view(), name='user-deposit-reset'),
]