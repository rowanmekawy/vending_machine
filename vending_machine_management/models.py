from django.db import models
from user_management.models import UserProfile

# Create your models here.
class Product(models.Model):
    amount_available = models.IntegerField()
    cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    product_name = models.CharField(max_length=255)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)