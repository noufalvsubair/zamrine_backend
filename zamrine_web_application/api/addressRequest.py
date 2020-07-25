from django.http import JsonResponse
from ..model.address import Address, AddressForm
from ..model.customer import Customer
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'mobile', 'address_type', 'city', 'country', 'house_name', 
            'landmark', 'pincode', 'state', 'street_name']

@csrf_exempt
def address(request):
    if request.method == 'POST' :
        response = {}
        requestBody = json.loads(request.body)
        userID = requestBody.get('user_id')
        if userID is not None:
            customer = Customer.objects.filter(id = userID).first()
            addressForm = AddressForm(requestBody)
            if customer is not None and addressForm.is_valid():
                print(addressForm)
                address = addressForm.save(commit = False)
                address.customer = customer
                addressForm.save()

                response = JsonResponse(data={'status': 'success', 
                    'message':'Address is added'})
                response.status_code = 201
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Customer does not exist'})
                response.status_code = 403
        else :
            response = JsonResponse(data={'status': 'error', 
                'message':'User ID was mandatory.'})
            response.status_code = 404

        return response

    if request.method == 'GET':
        response = {}
        userID = request.GET.get('id')
        if userID is not None:
            customer = Customer.objects.filter(id = userID).first()
            if customer is not None:
                addresses = Address.objects.filter(customer = customer)
                serializers = AddressSerializer(addresses, many=True)
                response = JsonResponse(serializers.data, safe=False)
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Customer does not exist'})
                response.status_code = 403
        else:
            response = JsonResponse(data={'status': 'error', 
                'message':'User ID was mandatory.'})
            response.status_code = 404
        
        return response

@csrf_exempt
def updateAddress(request):
    if request.method == 'POST':
        response = {}
        requestBody = json.loads(request.body)
        addressID = requestBody.get('id')
        if addressID is not None:
            address = Address.objects.filter(id = addressID).first()
            if address is not None :
                addressForm = AddressForm(requestBody, instance = address)
                addressForm.save()

                response = JsonResponse(data={'status': 'success', 
                    'message':'Address is updated'})
                response.status_code = 200 
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Address does not exist'})
                response.status_code = 403  
        else:
            response = JsonResponse(data={'status': 'error', 
                'message':'Address ID was mandatory.'})
            response.status_code = 404
    else:
        response = JsonResponse(data={'status': 'error', 'message':'Invalid request method.'})
        response.status_code = 404

    return response

@csrf_exempt
def removeAddress(request):
    if request.method == 'POST':
        response = {}
        addressID = request.POST.get('id')
        if addressID is not None:
            address = Address.objects.filter(id = addressID).first()
            if address is not None:
                address.delete()
                response = JsonResponse(data={'status': 'success', 
                    'message':'Address has removed'})
                response.status_code = 200
            else:
                response = JsonResponse(data={'status': 'fail', 
                    'message':'Address does not exist'})
                response.status_code = 403  
        else:
            response = JsonResponse(data={'status': 'error', 
                'message':'Address ID was mandatory.'})
            response.status_code = 404
    else:
        response = JsonResponse(data={'status': 'error', 'message':'Invalid request method.'})
        response.status_code = 404

    return response

