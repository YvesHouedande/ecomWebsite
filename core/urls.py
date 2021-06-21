from django.urls import path
from .views import (index, shop, product_detail,
				add_to_cart, checkout, account) 

app_name = 'core'
urlpatterns = [
	path('index/', index, name='Index-Page'),
	path('<str:shop_type>-Page/', shop, name='Shop-Page'),
	path('product/<klass>/<int:pk>/', product_detail, name='Product-Details'),
	path('add_to_cart/', add_to_cart, name='Adding-Cart'),
	path('checkout-page/', checkout, name='Checkout-Page'),
	path('login-page/', account, name='Login-Page'),
	path('register-page/', account, name='Register-Page')
	
]