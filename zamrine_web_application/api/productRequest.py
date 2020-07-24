from django.http import JsonResponse
from ..model.product import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    sizes = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'current_price', 'description', 'long_name', 
        'previous_price', 'soldBy', 'product_type', 'images', 'sizes']

def products(request):
    if request.method == 'GET':
        productType = request.GET.get('type')
        products = Product.objects.filter(product_type= productType)
        serializer = ProductSerializer(products, many=True)

        return JsonResponse(serializer.data, safe=False)