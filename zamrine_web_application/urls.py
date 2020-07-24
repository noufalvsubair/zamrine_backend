from django.conf.urls import url

from .api.productRequest import products
from .api.reviewRequest import reviews
from .api.userRequest import register, login
from .api.cartRequest import cart, updateCart, removeCart
from .api.addressRequest import address, updateAddress, removeAddress

urlpatterns = [
    url(r'^user/register.json', register),
    url(r'^user/login.json', login),
    url(r'^product.json', products),
    url(r'^product/reviews.json', reviews),
    url(r'^product/cart.json', cart),
    url(r'^product/update_cart.json', updateCart),
    url(r'^product/remove_cart.json', removeCart),
    url(r'^user/address.json', address),
    url(r'^user/update_address.json', updateAddress),
    url(r'^user/remove_address.json', removeAddress),
]