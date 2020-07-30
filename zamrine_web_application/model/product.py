from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length= 20, null=False, default="")
    current_price = models.IntegerField(default=0)
    description = models.TextField(null=True)
    short_name = models.CharField(max_length=20, null=False, default="")
    long_name = models.CharField(max_length=50, null=False, default= "")
    previous_price = models.IntegerField(default=0)
    soldBy = models.CharField(max_length=50, null=False, default="Zamrine")
    product_type = models.CharField(max_length=10, null=False, default="shop")
    action = "Edit"

    def __str__(self):
        return self.short_name

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, null=True)
    image_url = models.URLField(null=True)
    action = "Edit"

    def __str__(self):
        return self.image_url

class ProductSizes(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )
    
    product = models.ForeignKey(Product, related_name="sizes", null=True)
    size = models.CharField(max_length=2, choices=SIZES)
    action = "Edit"

    def __str__(self):
        return self.size