from django.conf.urls import url

from .api.productRequest import products
from .api.reviewRequest import reviews
from .api.userRequest import register

urlpatterns = [
    url(r'^product.json', products),
    url(r'^reviews.json', reviews),
    url(r'^register.json', register),
]