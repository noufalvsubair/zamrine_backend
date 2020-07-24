from django.conf.urls import url

from .api.productRequest import products
from .api.reviewRequest import reviews
from .api.userRequest import register, login
from .api.cartRequest import cart, updateCart

urlpatterns = [
    url(r'^user/register.json', register),
    url(r'^user/login.json', login),
    url(r'^product.json', products),
    url(r'^product/reviews.json', reviews),
    url(r'^product/cart.json', cart),
    url(r'^product/update_cart.json', updateCart),
]