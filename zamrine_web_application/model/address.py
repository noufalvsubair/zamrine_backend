from django.db import models
from .customer import Customer
from django import forms

class Address(models.Model):
    ADDRESS_TYPE = (
        ('H', 'Home(7 am - 9 pm delivery)'),
        ('O', 'Office/Commercial(10 am - 6 pm delivery)'),
    )

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=False, default= '')
    mobile = models.CharField(max_length=15, null=False, default= '')
    address_type = models.CharField(max_length=2, choices=ADDRESS_TYPE)
    city = models.CharField(max_length=100, null=False, default= '')
    country = models.CharField(max_length=50, null=False, default= '')
    house_name = models.CharField(max_length=200, null=False, default= '')
    landmark = models.CharField(max_length=100, null=False, default= '')
    pincode = models.CharField(max_length=10, null=False, default= '')
    state = models.CharField(max_length=50, null=False, default= '')
    street_name = models.CharField(max_length=200, null=True, default='')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address_type', 'city', 'country', 'house_name', 
            'landmark', 'pincode', 'state', 'street_name']
