from django.http import HttpResponse, JsonResponse
from ..model.customer import UserForm, CustomerForm
from django.views.decorators.csrf import csrf_exempt
import json
from ..serializers import UserSerializer

@csrf_exempt
def register(request):
    if request.method == 'POST':
        userForm = UserForm(json.loads(request.body))
        customerForm = CustomerForm(json.loads(request.body))
        if customerForm.is_valid() and userForm.is_valid():
            user = userForm.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customerForm.save()
            serializer = UserSerializer(user)
            response = JsonResponse(serializer.data, safe=False)
            response.status_code = 200
            return response
        else:
            response = JsonResponse(data={'status': 'error', 'message':'user has already registered'})
            response.status_code = 409
            return response