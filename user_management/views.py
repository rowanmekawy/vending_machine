import logging

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import UserProfileServices, TransactionServices
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

logger = logging.getLogger("django")

# Create your views here.
class UserCreateView(views.APIView):
    class UserCreateInputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        role = serializers.ChoiceField(choices=["seller", "buyer"])

    class UserCreateOutputSerializer(views.APIView):
        message = serializers.CharField(max_length=255)

    @extend_schema(
        description="create user",
        request=UserCreateInputSerializer,
        responses={201: UserCreateOutputSerializer()},
    )
    def post(self, request):
        logger.info(f"API: UsercreateView, request: {request.data}")
        input_serializer = self.UserCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            UserProfileServices().create(**input_serializer.validated_data)
        except Exception as e:    
            logger.error(f"API: UserCreateView, Error: {e}")
            return Response({"error": str(e)}, status=400)
        logger.info(f"API: User created successfully, request: {request.data}")
        return Response({"message": "User created successfully"}, status=201)
    
class UserUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    class UserUpdateInputSerializer(serializers.Serializer):
        username = serializers.CharField(required=False)
        role = serializers.ChoiceField(choices=["seller", "buyer"], required=False)

    class UserUpdateOutputSerializer(views.APIView):
        message = serializers.CharField(max_length=255)

    @extend_schema(
        description="Update user",
        request=UserUpdateInputSerializer,
        responses={200: UserUpdateOutputSerializer()},
    )
    def patch(self, request, pk):
        logger.info(f"API: UserUpdateView, request: {request.data}")
        input_serializer = self.UserUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserProfile, id=pk)
        try:
            UserProfileServices().update(user=user, data=input_serializer.validated_data)
        except Exception as e:   
            logger.error(f"API: UserUpdateView, Error: {e}") 
            return Response({"error": str(e)}, status=400)
        logger.info(f"API: User updated successfully, request: {request.data}")
        return Response({"message": "User updated successfully"}, status=200)    
    
class UserListView(views.APIView):
    permission_classes = [IsAuthenticated]

    class UserListOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        role = serializers.ChoiceField(choices=["seller", "buyer"])    

    @extend_schema(
        description="list all users",
        responses={200: UserListOutputSerializer(many=True)},
    )
    def get(self, request):    
        logger.info(f"API: UserListView, request: {request.user}")
        try:
            users = UserProfileServices().list()
        except Exception as e:
            logger.error(f"API: UserListView, Error: {e}")
            return Response({"error": str(e)}, status=400)
        output_serializer = self.UserListOutputSerializer(users, many=True)
        logger.info(f"API: UserListView, request Success: {request.user}")
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
class UserListDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    class UserListDetailOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        password = serializers.CharField()
        role = serializers.ChoiceField(choices=["seller", "buyer"])    

    @extend_schema(
        description="list user",
        responses={200: UserListDetailOutputSerializer()},
    )
    def get(self, request, pk):
        logger.info(f"API: User list, request: {request.data}")
        user = UserProfileServices().list_detial(user_id=pk)
        output_serializer = self.UserListDetailOutputSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_200_OK) 

class UserDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="delete user",
        responses={200: {}},
    )
    def delete(self, request, pk):
        UserProfileServices().delete(user_id=pk)
        logger.info(f"API: User deleted successfully, request: {request.data}")
        return Response({}, status=200)       
    
class UserBuyerDepositView(views.APIView):

    class UserBuyerDepositInputSerializer(serializers.Serializer):
        deposit_coins = serializers.ListField(
            child=serializers.ChoiceField(choices=["5", "10", "20", "50", "100"])
        )

    class UserBuyerDepositOutputSerializer(views.APIView):
        message = serializers.CharField(max_length=255)

    @extend_schema(
        description="UserBuyerDeposit",
        request=UserBuyerDepositInputSerializer,
        responses={200: UserBuyerDepositOutputSerializer()},
    )
    def post(self, request):
        logger.info(f"API: User Deposit request: {request.data}")
        if request.user.role != 'buyer':
            logger.error(f"API: User Deposit request, Error: user does not have buyer role")
            raise PermissionDenied
        input_serializer = self.UserBuyerDepositInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        deposit_coins = input_serializer.validated_data['deposit_coins']
        try:
            TransactionServices(user=request.user).deposit(deposit_coins=deposit_coins)
        except Exception as e:
            logger.error(f"API: User Deposit request, Error: {e}")
            return Response({"error": str(e)}, status=400)    
        logger.info(f"API: User Deposit request has done successfully, request: {request.data}")
        return Response({"message": "Deposit successful!"}, status=200)
    
class UserBuyerBuyView(views.APIView):

    class UserBuyerBuyInputSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        amount_of_products = serializers.IntegerField()

    class UserBuyerBuyOutputSerializer(serializers.Serializer): 
        product_id = serializers.IntegerField()
        total_amount = serializers.IntegerField()
        change_coins = serializers.DictField(
        child=serializers.IntegerField()
    )

    @extend_schema(
        description="UserBuyerDeposit",
        request=UserBuyerBuyInputSerializer,
        responses={200: UserBuyerBuyOutputSerializer()},
    )
    def post(self, request):
        logger.info(f"API: User Buy request: {request.data}")
        if request.user.role != 'buyer':
            logger.error(f"API: User Buy request, Error: user does not have buyer role")
            raise PermissionDenied
        input_serializer = self.UserBuyerBuyInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True) 
        try:
            data = TransactionServices(user=request.user).buy(**input_serializer.validated_data)
            output_serializer = self.UserBuyerBuyOutputSerializer(data)
            logger.info(f"API: User buy request has done successfully, request: {request.data}")
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"API: User buy request, Error: {e}")
            return Response({"error": str(e)}, status=400)    
        
           

class UserResetDepositView(views.APIView):

    @extend_schema(
        description="ResetDeposit",
        responses={200: {}},
    )
    def post(self, request):
        logger.info(f"API: User reset request: {request.data}")
        if request.user.role != 'buyer':
            logger.error(f"API: User reset request, Error: user does not have buyer role")
            raise PermissionDenied
        try:
            TransactionServices(user=request.user).reset()
        except Exception as e:
            logger.error(f"API: User reset request, Error: {e}")
            return Response({"error": str(e)}, status=400)    
        logger.info(f"API: User reset request has done successfully, request: {request.data}")
        return Response({"message": "Deposit Reseted successful!"}, status=200)           