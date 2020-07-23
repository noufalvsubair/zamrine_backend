from django.http import HttpResponse, JsonResponse
from ..model.product import Product
from ..serializers import ProductSerializer

def products(request):
    if request.method == 'GET':
        productType = request.GET.get('type')
        products = Product.objects.filter(product_type= productType)
        serializer = ProductSerializer(products, many=True)

        return JsonResponse(serializer.data, safe=False)