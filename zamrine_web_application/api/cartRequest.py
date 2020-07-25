from django.http import JsonResponse
from ..model.cart import Cart, CartForm
from ..model.product import Product
from ..model.customer import Customer
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from .productRequest import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)

    class Meta:
        model = Cart
        fields = ['id', 'size', 'quantity', 'product']

def calculateOverAllPrice(cartItems):
    overAllCost = 0
    for cart in cartItems:
        productPrice = cart.product.current_price
        productQuantity = cart.quantity
        overAllCost = overAllCost + (productPrice * productQuantity)
        
    return overAllCost

def calculateOverAllDiscount(cartItems):
    overAllDiscount = 0
    for cart in cartItems:
        productPrice = cart.product.current_price
        productPreviousPrice = cart.product.previous_price
        productQuantity = cart.quantity
        if (productPreviousPrice > 0):
            overAllDiscount = overAllDiscount + ((productPreviousPrice 
                - productPrice) * productQuantity)
        
    return overAllDiscount

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
                    'message':'Product does not exist'})
            response.status_code = 403   

        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID & User ID was mandatory'})
            response.status_code = 403

        return response
    
    if request.method == 'GET':
        userID = request.GET.get('id')
        response = {}
        if userID is not None:
            customer = Customer.objects.filter(id = userID).first()
            if customer is not None:
                cartItems = Cart.objects.filter(customer = customer)
                serializers = CartSerializer(cartItems, many=True)
                response['total_price'] = calculateOverAllPrice(cartItems = cartItems)
                response['total_discount'] = calculateOverAllDiscount(cartItems = cartItems)
                response['delivery_charge'] = 0
                response['cart_items'] = serializers.data
                response = JsonResponse(response, safe=False)
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Customer does not exist'})
                response.status_code = 403   
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'User ID was mandatory'})
            response.status_code = 403
        
        return response

@csrf_exempt
def updateCart(request):
    if request.method == 'POST':
        response = {}
        requestBody = json.loads(request.body)
        cartID = requestBody.get('id')
        quantity = requestBody.get('quantity')
        if cartID is not None and quantity is not None:
            cartitem = Cart.objects.filter(id = cartID).first()
            if cartitem is not None:
                if (cartitem.quantity < 3 and quantity < 3):
                    cartitem.quantity = quantity
                    cartitem.save(update_fields=['quantity'])
                    response = JsonResponse(data={'status': 'success', 
                        'message':'Cart item is updated'})
                    response.status_code = 200 
                else :
                    response = JsonResponse(data={'status': 'fail', 
                        'message':'Maxium cart was item quantity exceeded'})
                    response.status_code = 304
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Cart Item does not exist'})
                response.status_code = 403
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Cart ID & Quantity was mandatory'})
            response.status_code = 403
    else:
        response = JsonResponse(data={'status': 'error', 'message':'Invalid request method.'})
        response.status_code = 404

    return response

@csrf_exempt
def removeCart(request):
    if request.method == 'POST':
        response = {}
        cartID = request.POST.get('id')
        if cartID is not None:
            cartItem = Cart.objects.filter(id = cartID).first()
            if cartItem is not None:
                cartItem.delete()
                response = JsonResponse(data={'status': 'success', 
                    'message':'Cart Item was removed'})
                response.status_code = 200
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Cart Item does not exist'})
                response.status_code = 403
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Cart ID was mandatory'})
            response.status_code = 403
    
    else:
        response = JsonResponse(data={'status': 'error', 'message':'Invalid request method.'})
        response.status_code = 404

    return response
