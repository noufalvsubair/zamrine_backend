from django.http import JsonResponse
from ..model.product import Product, ProductImages
from .reviewRequest import ReviewSerializer, Reviews
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
        

class ProductDetailsSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    sizes = serializers.StringRelatedField(many=True)
    offer = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'current_price', 'description', 'long_name', 'short_name',
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

def calculateOverAllRating(reviews):
    rating = 0
    for review in reviews:
        rating = rating + review.rating

    return  rating / len(reviews) if (rating > 0) else 0

def calculateRatingCount(reviews):
    ratingCount = 0
    for review in reviews:
        ratingCount = ratingCount + review.rating
    
    return int(math.floor(ratingCount))

def productDetails(request, product_id):
    if request.method == 'GET':
        if product_id is not None:
            product = Product.objects.filter(id = product_id).first()
            if product is not None:
                reviews = Reviews.objects.filter(product = product)
                relatedProducts = Product.objects.filter(product_type = product.product_type 
                    or soldBy == product.soldBy).exclude(id = product.id)[:4]

                serializers = ProductDetailsSerializer(product)
                relatedProductSerializer = ProductListSerializer(relatedProducts, many=True)
                reviewSerializer = ReviewSerializer(reviews.first())

                response = serializers.data
                response['review'] = reviewSerializer.data if (len(reviews) > 0) else None
                response['rating'] = float(calculateOverAllRating(reviews = reviews))
                response['rating_count'] = int(calculateRatingCount(reviews = reviews))
                response['related_product'] = relatedProductSerializer.data

                response = JsonResponse(response, safe=False)
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Product does not exist'})
                response.status_code = 404
        else: 
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID was mandatory'})
            response.status_code = 403

    return response   


