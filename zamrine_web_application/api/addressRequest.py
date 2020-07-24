from django.http import JsonResponse
from ..model.address import Address, AddressForm
from ..model.customer import Customer
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address_type', 'city', 'country', 'house_name', 
            'landmark', 'pincode', 'state', 'street_name']

@csrf_exempt
def address(request):
    if request.method == 'POST' :
        response = {}
        requestBody = json.loads(request.body)
        userID = requestBody.get('user_id')
        if userID is not None:
            customer = Customer.objects.filter(id = userID).first()
            if customer is not None :
                addressForm = AddressForm(requestBody)
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
        requestBody = json.loads(request.body)
        userID = requestBody.get('id')
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
