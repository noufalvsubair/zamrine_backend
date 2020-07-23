from django.conf.urls import url

from .api.productRequest import products
from .api.reviewRequest import reviews

urlpatterns = [
    url(r'^product.json', products),
    url(r'^reviews.json', reviews)
]