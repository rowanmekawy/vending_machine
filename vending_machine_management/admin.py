from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("id", "amount_available", "seller", "cost")
    list_filter = ("id",)
    search_fields = ["id", ] 