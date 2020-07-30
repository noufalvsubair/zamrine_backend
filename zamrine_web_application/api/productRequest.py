from django.http import JsonResponse
from ..model.product import Product
from .reviewRequest import ReviewSerializer
from rest_framework import serializers
import math

class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    offer = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'short_name' ,'current_price', 'previous_price', 'offer', 'images']

    def get_offer(self, obj):
        offer = 0
        if (obj.previous_price > 0):
            offer = math.floor((obj.previous_price - obj.current_price) /100)
        
        return int(offer)

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    sizes = serializers.StringRelatedField(many=True)
    offer = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'current_price', 'description', 'long_name', 'short_name' 
        'previous_price', 'soldBy', 'product_type', 'images', 'sizes', 'offer']

    def get_offer(self, obj):
        offer = 0
        if (obj.previous_price > 0):
            offer = math.floor((obj.previous_price - obj.current_price) /100)
        
        return int(offer)


def products(request):
    if request.method == 'GET':
        productType = request.GET.get('type')
        products = Product.objects.filter(product_type= productType)
        serializer = ProductListSerializer(products, many=True)

        return JsonResponse(serializer.data, safe=False)

def relatedProducts(request):
    if request.method == 'GET':
        response = {}
        productID = request.GET.get('id')
        if productID is not None:
            product = Product.objects.filter(id = productID).first()
            if product is not None:
                relatedProducts = Product.objects.get(Q(product_type = product.product_type)
                    | Q(category = product.category) | Q(soldBy = product.soldBy) & Q(id != product.id))
                serializers = ProductSerializer(relatedProducts, many=True)
                response = JsonResponse(serializers.data, safe=False)
                response.status_code = 200
            else:
                response = JsonResponse(data = {'status': 'fail', 
                    'message': 'Product does not exist'})
                response.status_code = 404

        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID was mandatory'})
            response.status_code = 403

        return response

    


