from django.http import JsonResponse
from ..model.review import Reviews, ReviewForm
from ..model.product import Product
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'created_at', 'title', 'image_url', 'message', 'name', 'rating']

@csrf_exempt
def reviews(request):
    if request.method == 'GET':
        productID = request.GET.get('product_id')
        if productID is None :
            response = JsonResponse(data={'status': 'error', 'message':'Product ID was mandatory.'})
            response.status_code = 404
            return response

        else :
            product = Product.objects.get(id= productID)
            reviews = Reviews.objects.filter(product= product)
            serializer = ReviewSerializer(reviews, many=True)

            return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        requestBody = json.loads(request.body)
        productID = requestBody.get('id')
        response = {}
        if productID is not None :
            product = Product.objects.filter(id = productID).first()
            
            if product is not None :
                reviewForm = ReviewForm(requestBody)
                review = reviewForm.save(commit=False)
                review.product = product
                reviewForm.save()

                response = JsonResponse(data={'status': 'success', 
                    'message':'Review is added.'})
                response.status_code = 201

            else :
                response = JsonResponse(data={'status': 'success', 
                    'message':'Please provide valid product ID.'})
                response.status_code = 403

        else:
            response = JsonResponse(data={'status': 'error', 
                'message':'Product ID was mandatory.'})
            response.status_code = 404
    
    return response




