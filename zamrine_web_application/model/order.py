from django.db import models
from .address import Address
from .customer import Customer
from .product import Product
from uuid import uuid4

class Order(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )

    id = models.CharField(max_length=8, null= False, unique=True, primary_key=True, default='')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, db_index=True, null=True)
    payment_method = models.CharField(max_length=50, null=False, default='')
    price = models.IntegerField(default=0)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, db_index=True, null=True)
    product_size = models.CharField(max_length=2, choices=SIZES)
    quantity = models.IntegerField(default=0, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)