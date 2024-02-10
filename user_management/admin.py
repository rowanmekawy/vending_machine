from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ("id", "role")
    list_filter = ("role",)
    search_fields = ["id", ]

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ("id", "reset", "transaction_type", "amount")
    list_filter = ("reset",)
    search_fields = ["id", ]    