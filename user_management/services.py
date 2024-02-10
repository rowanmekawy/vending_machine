from django.db import transaction
from .models import UserProfile, Transaction
from vending_machine_management.models import Product
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class UserProfileServices:
    def create(self, username, password, role):
        return UserProfile.objects.create(
            username=username, password=password, role=role
        )
    
    def list(self):
        return UserProfile.objects.all()
    
    def list_detial(self, user_id):
        return get_object_or_404(UserProfile, id=user_id)
    
    def delete(self, user_id):
        user = get_object_or_404(UserProfile, id=user_id)
        user.delete()

    def update(self, user:UserProfile, data):
        for field, value in data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        user.save()
        return user    
    
class TransactionServices:
    def __init__(self, user) -> None:
        self.user = user

    @transaction.atomic
    def deposit(self, deposit_coins):
        total = sum(int(x) for x in deposit_coins)
        new_transaction = Transaction.objects.create(user=self.user, amount=total, transaction_type="in")
        self.user.deposit += new_transaction.amount
        self.user.save()

    def reset(self):
        self.user.deposit = 0
        self.user.save()    
        transactions =Transaction.objects.filter(user=self.user, reset=False)
        for transaction in transactions:
            transaction.reset = True
            transaction.save()

    def calculate_change_breakdown(self, change):
        coin_denominations = [100, 50, 20, 10, 5]
        change_breakdown = {}

        for denomination in coin_denominations:
            num_coins = change // denomination
            if num_coins > 0:
                change_breakdown[str(denomination)] = int(num_coins)
                change -= num_coins * denomination
        return change_breakdown

    @transaction.atomic
    def buy(self, product_id, amount_of_products):
        product = get_object_or_404(Product, id=product_id)
        total_amount = product.cost * amount_of_products
        if total_amount > self.user.deposit:
            raise ValidationError("Insufficient funds")
        if product.amount_available < amount_of_products:
            raise ValidationError("No Avaliable Stock")
        self.user.deposit -= total_amount
        self.user.save()
        Transaction.objects.create(
            user=self.user,
            amount=total_amount,
            transaction_type='out',
        )
        product.amount_available -= amount_of_products
        product.save()
        change_breakdown = {}
        if self.user.deposit > 0:
            change = self.user.deposit
            change_breakdown = self.calculate_change_breakdown(change=change)
        payload = {
            "product_id": product_id,
            "total_amount": int(total_amount),
            "change_coins": change_breakdown
        } 
        return payload

        
            