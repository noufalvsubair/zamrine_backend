from rest_framework import serializers
from .model.product import Product
from .model.review import Reviews
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    sizes = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'current_price', 'description', 'long_name', 
        'previous_price', 'soldBy', 'product_type', 'images', 'sizes']

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'created_at', 'title', 'image_url', 'message', 'name', 'rating']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    mobile = serializers.CharField(source='customer.mobile')
    auth_token = serializers.CharField(source='customer.auth_token')
    image_url = serializers.CharField(source='customer.image_url')
    id = serializers.IntegerField(source='customer.id')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'mobile', 
            'auth_token', 'image_url']