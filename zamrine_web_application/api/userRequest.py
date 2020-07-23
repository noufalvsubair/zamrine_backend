from django.http import HttpResponse, JsonResponse
from ..model.customer import Customer, UserForm, CustomerForm
from django.views.decorators.csrf import csrf_exempt
import json

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
            response = JsonResponse(data={'status': 'success', 'message':'user has registered'})
            response.status_code = 200
            return response
        else:
            response = JsonResponse(data={'status': 'error', 'message':'user has already registered'})
            response.status_code = 409
            return response
