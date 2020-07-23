from rest_framework import serializers
from .model.product import Product
from .model.review import Reviews

class ProductSerializer(serializers.HyperlinkedModelSerializer):
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