from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserProfileManager

# Create your models here.

class UserProfile(AbstractBaseUser, PermissionsMixin):
    deposit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    role = models.CharField(max_length=20, choices=[('seller', 'Seller'), ('buyer', 'Buyer')])
    username =  models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="user_profile_set",
        related_query_name="user_profile",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_profile_set",
        related_query_name="user_profile",
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[('in', 'In'), ('out', 'Out')])
    reset = models.BooleanField(default=False)