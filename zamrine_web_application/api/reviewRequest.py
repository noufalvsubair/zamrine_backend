from django.http import HttpResponse, JsonResponse
from ..serializers import ReviewSerializer
from ..model.review import Reviews

def reviews(request):
    if request.method == 'GET':
        productID = request.GET.get('product_id')
        if productID is None :
            response = JsonResponse(data={'status': 'error', 'message':'product id was mandatory'})
            response.status_code = 404
            return response
        else :
            product = Product.objects.get(id= productID)
            reviews = Reviews.objects.filter(product= product)
            serializer = ReviewSerializer(reviews, many=True)

            return JsonResponse(serializer.data, safe=False)
    
    # if request.method == 'POST':