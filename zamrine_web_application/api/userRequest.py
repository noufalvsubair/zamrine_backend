from django.http import JsonResponse
from ..model.customer import UserForm, CustomerForm
from django.views.decorators.csrf import csrf_exempt
import json
from ..serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

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
            serializer = UserSerializer(user)
            response = JsonResponse(serializer.data, safe=False)
            response.status_code = 200
            return response
        else:
            response = JsonResponse(data={'status': 'error', 'message':'user has already registered'})
            response.status_code = 409
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
            
