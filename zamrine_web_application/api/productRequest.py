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

    


