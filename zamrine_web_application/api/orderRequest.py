from django.http import JsonResponse
from ..model.order import Order, OrderStatus, OrderForm, OrderStatusFom
from ..model.customer import Customer
from ..model.product import Product
from ..model.address import Address
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
import time
import json
from rest_framework import serializers

class OrderProductSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ['id', 'long_name', 'soldBy', 'images']

class OrderStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['status', 'created_at']

class OrderListSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer(read_only = True)
    status = OrderStatusSerializer(read_only = True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'price', 'product', 'status']

@csrf_exempt
def order(request):
    if request.method == 'POST':
        requestBody = json.loads(request.body)
        productID = requestBody.get('id')
        userID = requestBody.get('user_id')
        addressID = requestBody.get('address_id')
        if productID is not None and userID is not None and addressID is not None:
            customer = Customer.objects.filter(id = userID).first()
            product = Product.objects.filter(id = productID).first()
            address = Address.objects.filter(id = addressID).first()
            if product is not None and customer is not None and address is not None:
                orderForm = OrderForm(requestBody)
                order = orderForm.save(commit=False)
                order.id = int(time.time())
                order.product = product
                order.price = product.current_price
                order.customer = customer
                order.address = address
                orderForm.save()

                orderStatusForm = OrderStatusFom({'status': 'ordered'})
                orderStatus = orderStatusForm.save(commit=False)
                orderStatus.order = order
                orderStatusForm.save()

                response = JsonResponse(data={'status': 'success', 
                    'message':'Product is purchased'})
                response.status_code = 201
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Product does not exist'})
                response.status_code = 404
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID, User ID & address ID was mandatory'})
            response.status_code = 403
        
        return response
    
    if request.method == 'GET':
        userID = request.GET.get('id')
        if userID is not None:
            customer = Customer.objects.filter(id = userID).first()
            if customer is not None:
                orders = Order.objects.filter(customer = customer)
                serializer = OrderListSerializer(orders, many=True)
                response = JsonResponse(serializer.data, safe=False)
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Customer does not exist'})
                response.status_code = 404
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'User ID was mandatory'})
            response.status_code = 403
        
        return response

@csrf_exempt
def hasPurchased(request):
    if request.method == 'POST':
        requestBody = json.loads(request.body)
        productID = requestBody.get('id')
        userID = requestBody.get('user_id')
        if userID is not None and productID is not None:
            currentUser = Customer.objects.filter(id=userID).first()
            product = Product.objects.filter(id=productID).first()
            if currentUser is not None and product is not None:
                userOder = Order.objects.filter(product=product).filter(customer=currentUser).first()
                purchased = userOder is not None
                response = JsonResponse(data={'status': 'success', 
                    'has_purchased': purchased})
                response.status_code = 200
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Customer or Product does not exist'})
                response.status_code = 404 
        else:
            response = JsonResponse(data={'status': 'fail', 
                    'message':'Product ID & User ID  was mandatory'})
            response.status_code = 403

        return response
