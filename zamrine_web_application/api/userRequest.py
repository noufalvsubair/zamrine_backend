from django.http import JsonResponse
from ..model.customer import UserForm, CustomerForm, Customer
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
import pyotp
from django.core.mail import send_mail

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
            response.status_code = 201
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
            currentCustomer = Customer.objects.filter(mobile= mobile).first()
            if currentUser is not None and currentCustomer is not None:
                currentCustomer.email_otp = pyotp.TOTP(pyotp.random_base32()).now()
                currentCustomer.mobile_otp = pyotp.TOTP(pyotp.random_base32()).now()
                currentCustomer.save(update_fields=['email_otp', 'mobile_otp'])

                # html_content = '<p>To activate your zamrine account, Please verify your email address.<br> Your acccount will not be created until your email address id confirmed <br> OTP: <strong>'+ currentCustomer.email_otp +'</strong>>'
                # send_mail(subject='Verify your email', 
                #     from_email='no-reply@zamrine.com', 
                #     recipient_list=[email], message='', html_message=html_content, fail_silently=False)

                response = JsonResponse(data={'status': 'success', 'mobile_otp': currentUser.customer.mobile_otp, 
                    'email_otp': currentUser.customer.email_otp,
                    'message':"We have sent the OTP. Please check your email & mobile"})
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
    
    if request.method == 'POST':
        requestBody = json.loads(request.body)
        response = {}
        email = requestBody.get('email')
        mobile = requestBody.get('mobile')
        emailOTP = requestBody.get('email_otp')
        mobileOTP = requestBody.get('mobile_otp')
        if mobile is not None and email is not None :
            currentUser = User.objects.filter(username= email).first()
            currentCustomer = Customer.objects.filter(mobile=mobile).filter(email_otp=emailOTP).filter(mobile_otp=mobileOTP).first()
            print(currentUser)
            if currentUser is not None and currentCustomer is not None:
                currentCustomer.is_mobile_verifiied = True
                currentCustomer.is_email_verified = True
                currentCustomer.save(update_fields=['is_mobile_verifiied', 'is_email_verified'])

                serializer = UserSerializer(currentUser)
                response = JsonResponse(serializer.data, safe=False)
                response.status_code = 200

            else:
                response = JsonResponse(data={'status': 'error', 
                    'message':"Could you please check the data"})
                response.status_code = 404
        else :
            response = JsonResponse(data={'status': 'error', 
                'message':'Please enter valid mobile & email'})
            response.status_code = 409
        
        return response

            
