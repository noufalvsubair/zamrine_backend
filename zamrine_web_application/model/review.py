from django.db import models
from .product import Product
from django import forms

class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=20, null=True)
    image_url = models.URLField(null=True)
    message = models.TextField(null=False, default="")
    name = models.CharField(max_length=40, null=False, default="")
    rating = models.DecimalField(decimal_places=2, max_digits=3)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['title', 'image_url', 'message', 'name', 'rating']