from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, response, serializers, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .services import ProductServices
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# Create your views here.
class ProductCreateView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    class ProductCreateOutputSerializer(views.APIView):
        message = serializers.CharField(max_length=255)

    @extend_schema(
        description="create product",
        request=serializer_class,
        responses={201: ProductCreateOutputSerializer()},
    )
    def post(self, request):
        if request.user.role != 'seller':
            raise PermissionDenied
        input_serializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            ProductServices().create(**input_serializer.validated_data)
        except Exception as e:    
            return Response({"error": str(e)}, status=400)
        return Response({"message": "Product created successfully"}, status=201)
    
class ProductUpdateView(views.APIView):

    class ProductUpdateInputSerializer(serializers.Serializer):
        amount_available = serializers.IntegerField(required=False)
        cost = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
        product_name = serializers.CharField(required=False)

    class ProductUpdateOutputSerializer(views.APIView):
        message = serializers.CharField(max_length=255)

    @extend_schema(
        description="Update user",
        request=ProductUpdateInputSerializer,
        responses={200: ProductUpdateOutputSerializer()},
    )
    def patch(self, request, pk):
        if request.user.role != 'seller':
            raise PermissionDenied
        input_serializer = self.ProductUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = get_object_or_404(Product, id=pk)
        try:
            ProductServices().update(user=user, data=input_serializer.validated_data)
        except Exception as e:    
            return Response({"error": str(e)}, status=400)
        return Response({"message": "Product updated successfully"}, status=200)    
    
class ProductListView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    @extend_schema(
        description="list all users",
        responses={200: serializer_class(many=True)},
    )
    def get(self, request):    
        try:
            users = ProductServices().list()
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        output_serializer = self.serializer_class(users, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
class ProductListDetailView(views.APIView):
    serializer_class = ProductSerializer  

    @extend_schema(
        description="list producr",
        responses={200: serializer_class()},
    )
    def get(self, request, pk):
        producr = ProductServices().list_detial(product_id=pk)
        output_serializer = self.serializer_class(producr)
        return Response(output_serializer.data, status=status.HTTP_200_OK) 

class ProductDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="delete product",
        responses={200: {}},
    )
    def delete(self, request, pk):
        if request.user.role != 'seller':
            raise PermissionDenied
        ProductServices().delete(product_id=pk)
        return Response({}, status=200)       