from django.http import JsonResponse
from ..model.customer import UserForm, CustomerForm
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
import pyotp

class UserSerializer(serializers.HyperlinkedModelSerializer):
    mobile = serializers.CharField(source='customer.mobile')
    auth_token = serializers.CharField(source='customer.auth_token')
    image_url = serializers.CharField(source='customer.image_url')
    id = serializers.IntegerField(source='customer.id')
    is_mobile_verifiied = serializers.BooleanField(source='customer.is_mobile_verifiied')
    is_email_verified = serializers.BooleanField(source='customer.is_email_verified')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'mobile', 
            'auth_token', 'image_url', 'is_mobile_verifiied', 'is_email_verified']

@csrf_exempt
def register(request):
    if request.method == 'POST':
        userForm = UserForm(json.loads(request.body))
        customerForm = CustomerForm(json.loads(request.body))
        if customerForm.is_valid() and userForm.is_valid():
            user = userForm.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.auth_token = Token.objects.create(user= user).key
            customerForm.save()
        
            response = JsonResponse(data={'status': 'success', 'message':'user has registered'})
            response.status_code = 200
        else:
            response = JsonResponse(data={'status': 'error', 'message':'user has already registered'})
            response.status_code = 409
    else:
        response = JsonResponse(data={'status': 'error', 'message':'Invalid request method.'})
        response.status_code = 404
        
    return response


@csrf_exempt
def login(request):
    if request.method == 'POST':
        requestBody = json.loads(request.body)
        username = requestBody.get('username')
        password = requestBody.get('password')

        if username is not None or password is not None :
            user = authenticate(username = username, password = password)
            if user is not None:
                serializer = UserSerializer(user)
                response = JsonResponse(serializer.data, safe=False)
                response.status_code = 200
                return response
            else:
                response = JsonResponse(data={'status': 'error', 'message':"User account does't exist"})
                response.status_code = 404
                return response
        else :
            response = JsonResponse(data={'status': 'error', 'message':'Please enter valid username & password'})
            response.status_code = 409
            return response
    else:
        response = JsonResponse(data={'status': 'error', 'message':'Invalid request method.'})
        response.status_code = 404
        
    return response

@csrf_exempt
def otp(request):
    if request.method == 'GET':
        mobile = request.GET.get('mobile')
        email = request.GET.get('email')
        response = {}
        if mobile is not None and email is not None:
            currentUser = User.objects.filter(username=email).first()
            if currentUser is not None:
                hotp = pyotp.HOTP('base32secret3232')
                print("Current Email OTP:", pyotp.HOTP(pyotp.random_hex()).now())
                print("Current Mobile OTP:", pyotp.HOTP(pyotp.random_hex()).now())

                response = JsonResponse(data={'status': 'success', 
                    'message':"We have sent the OTP"})
                response.status_code = 200
            else:
                response = JsonResponse(data={'status': 'error', 
                    'message':"User account does't exist"})
                response.status_code = 404
        else:
            response = JsonResponse(data={'status': 'error', 
                'message':'Please enter valid mobile & email'})
            response.status_code = 409
        
        return response

            
