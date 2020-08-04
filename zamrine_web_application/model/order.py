from django.db import models
from .address import Address
from .customer import Customer
from .product import Product
from django import forms

class Order(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )

    id = models.CharField(max_length=20, null= False, unique=True, primary_key=True, default='')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, db_index=True, null=True)
    payment_method = models.CharField(max_length=50, null=False, default='')
    price = models.IntegerField(default=0)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, db_index=True, null=True)
    product_size = models.CharField(max_length=2, choices=SIZES)
    quantity = models.IntegerField(default=0, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)


class OrderStatus(models.Model):
    STATUS = (
        ('ordered', 'Ordered'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status", null=True)
    status = models.CharField(max_length=30, choices=STATUS)
    created_at = models.DateTimeField(auto_now=True)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('payment_method', 'product_size', 'quantity')

class OrderStatusFom(forms.ModelForm):
    class Meta:
        model = OrderStatus
        fields = ('status',)