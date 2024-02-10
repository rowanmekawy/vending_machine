from .models import Product
from django.shortcuts import get_object_or_404

class ProductServices:
    def create(self, amount_available, cost, product_name, seller):
        return Product.objects.create(
            amount_available=amount_available, cost=cost, product_name=product_name, seller=seller
        )
    
    def list(self):
        return Product.objects.all()
    
    def list_detial(self, product_id):
        return get_object_or_404(Product, id=product_id)
    
    def delete(self, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()

    def update(self, product:Product, data):
        for field, value in data.items():
            if hasattr(product, field):
                setattr(product, field, value)
        product.save()
        return product    