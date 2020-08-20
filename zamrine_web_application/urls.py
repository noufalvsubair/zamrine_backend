from django.conf.urls import url

from .api.productRequest import products, productDetails
from .api.reviewRequest import reviews
from .api.userRequest import register, login, otp
from .api.cartRequest import cart, updateCart, removeCart
from .api.addressRequest import address, updateAddress, removeAddress
from .api.orderRequest import order, hasPurchased

urlpatterns = [
    url(r'^user/register.json', register),
    url(r'^user/login.json', login),
    url(r'^user/otp.json', otp),
    url(r'^product.json', products),
    url(r'^product/(?P<product_id>\w{0,50}).json/$', productDetails),
    url(r'^product/reviews.json', reviews),
    url(r'^product/cart.json', cart),
    url(r'^product/update_cart.json', updateCart),
    url(r'^product/(?P<cart_id>\w{0,50})/remove_cart.json', removeCart),
    url(r'^user/address.json', address),
    url(r'^user/update_address.json', updateAddress),
    url(r'^user/(?P<addressID>\w{0,50})/remove_address.json', removeAddress),
    url(r'^user/order.json', order),
    url(r'^user/order/purchased.json', hasPurchased),
]