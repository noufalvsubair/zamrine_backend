from django.db import models
from .product import Product
from django import forms
from .customer import Customer

class Cart(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )

    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, db_index=True, null=True)
    size = models.CharField(max_length=2, choices=SIZES)
    quantity = models.IntegerField(default=0, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['size', 'quantity']