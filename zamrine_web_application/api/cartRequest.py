from django.http import JsonResponse
from ..model.cart import Cart, CartForm
from ..model.product import Product
from ..model.customer import Customer
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from ..serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)

    class Meta:
        model = Cart
        fields = ['size', 'quantity', 'product']

@csrf_exempt
def cart(request):    
    if request.method == 'POST':
        response = {}
        requestBody = json.loads(request.body)
        productID = requestBody.get('id')
        userID = requestBody.get('user_id')
        if userID is not None and productID is not None :
            customer = Customer.objects.filter(id = userID).first()
            product = Product.objects.filter(id = productID).first()
            if product is not None and customer is not None:
                cartForm = CartForm(requestBody)
                cart = cartForm.save(commit= False)
                cart.product = product
                cart.customer = customer
                cartForm.save()

                response = JsonResponse(data={'status': 'success', 
                    'message':'Product is added to cart'})
                response.status_code = 201
            else:
             response = JsonResponse(data={'status': 'fail', 
                    'message':'Please provide a valid user & product'})
            response.status_code = 403   

        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID & User ID was mandatory'})
            response.status_code = 403

        return response
    
    if request.method == 'GET':
        userID = request.GET.get('id')
        if userID is not None:
            customer = Customer.objects.filter(id = userID).first()
            if customer is not None:
                cartItems = Cart.objects.filter(customer = customer)
                serializers = CartSerializer(cartItems, many=True)
                response = JsonResponse(serializers.data, safe=False)
            else:
             response = JsonResponse(data={'status': 'fail', 
                    'message':'Please provide a valid user'})
            response.status_code = 403   
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID & User ID was mandatory'})
            response.status_code = 403
        
        return response