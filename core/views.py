from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login
from .models import (Product, ClotheProduct, 
					AccessorieProduct, CosmeticProduct,
					Category, Image, Order, OrderProduct, Customer)
# Some Tries
from random import randint
from .forms import BillingInfoForm, AccountForm
# from django.session.db.models import Session 
	 
# Create your views here.

def index(request):
	queryset = Product.all_products(ClotheProduct, AccessorieProduct,
	CosmeticProduct, featured=True, is_new=True)
	men_cat_nb = len([x for x in queryset if x.gender == 'Male' or x.gender=='Both']) 
	kid_cat_nb = len([x for x in queryset if x.for_kid == 'Yes'])
	cosmetic_nb = CosmeticProduct.objects.all().count()
	Accessorie_nb = AccessorieProduct.objects.all().count()
	order_quantity = 0 if not 'order_quantity' in request.session else request.session['order_quantity']
	context = {
		'order_quantity':order_quantity,
		'Accessorie_nb':Accessorie_nb,
		'cosmetic_nb':cosmetic_nb,
		'men_cat_nb':men_cat_nb,
		'kid_cat_nb':kid_cat_nb,
		'items':queryset
	}
	return render(request, 'index.html', context)

# for the shop view
def clothe_categories():
	clothe_categories = {
	'Women':'One',
	'Men':'Two',
	'kid':'Three'
	}
	return clothe_categories.items()

# help cause of cat men=Male, women=female
_gender = lambda gender: 'Men' if gender == 'Male' else 'Women'

def shop(request, shop_type):
	queryset = Product.all_products(ClotheProduct, AccessorieProduct,
	CosmeticProduct)
	# if shop, we have the full products
	if shop_type != 'Shop':
		queryset = [prdt for prdt in queryset if _gender(prdt.gender) == shop_type]
	paginate = Paginator(queryset, 3)
	try:
		page_num = int(request.GET.get('page')) 
	except:
		page_num = 1
	
	order_quantity = 0 if not 'order_quantity' in request.session else request.session['order_quantity']
	context = {
		'order_quantity':order_quantity,
		'shop_type':shop_type,
		'paginate':paginate,
		'page':paginate.page(page_num),
		'close_categories':	clothe_categories(),
		 }
	return render(request, 'shop.html', context)


def product_detail(request, klass, pk):
	klasses = [ClotheProduct, AccessorieProduct, CosmeticProduct]
	product = [kls.objects.filter(pk=pk).first() for kls in klasses if kls.__name__ == klass][0]
	imgs = Image.objects.filter(product=product.id) or None
	order_quantity = 0 if not 'order_quantity' in request.session else request.session['order_quantity']
	# request.session['order_quantity'] = 0
	context = {
		'order_quantity':order_quantity,
		'product':product,
		'imgs':imgs,
		# 'CosmeticProduct':CosmeticProduct,
	}
	return render(request, 'product-details.html', context)

cart_name = 'card_id'
def _generate_cart_id():
	"""
	this will use to generate card id for non customer
	"""    
	cart_id = ''      
	characters = 'ABCDEFGHIJKLMNOPQRQSTUVWXYZabcdefghij\
	klmnopqrstuvwxyz1234567890!@#$%^&*()'      
	cart_id_length = 50      
	for y in range(cart_id_length):           
		cart_id += characters[randint(0, len(characters)-1)]      
	return cart_id

def session_order(request):
	if not cart_name in request.session:
		request.session[cart_name] = _generate_cart_id()
	return request.session[cart_name]

	
@csrf_exempt
def add_to_cart(request):
	""" je comprends ici que python n'est pas assez perfommant pour creer des 
		application temps réel, en effet, en faisant des requetes multiples, il y' a des 
		abandons.
	"""
	data = json.loads(request.body)
	# getting the product by his category called klass and some data in var data
	klass = data.get('category')
	klasses = [ClotheProduct, AccessorieProduct, CosmeticProduct]
	product = [kls.objects.filter(pk=data.get('productId')).first() for kls in klasses if kls.__name__ == klass][0]
	# only user will have an order,otherwise ...
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer)
		order.quantity = data.get('order_quantity')
		order.save()
		# creating an order product ignoring his quantity
		order_product, created = OrderProduct.objects.get_or_create(category=data.get('category'), name=product.name,
		color=data.get('color'), size=data.get('size'), order=order,
		price=product.real_price())
	else:
		order_product, created = OrderProduct.objects.get_or_create(category=data.get('category'), name=product.name,
		color=data.get('color'), size=data.get('size'), session_order=session_order(request),
		price=product.real_price())
	# updating order_quantity
	order_product.quantity += (int(data.get('input')) - 1) if created else int(data.get('input'))
	order_product.save()
	# put cart quantity in session making it accessible from all views
	request.session['order_quantity'] = data.get('order_quantity')
	print(request.session['order_quantity'])
	return JsonResponse('data updated', safe=False)
 
def checkout(request):
	user = request.user.is_authenticated
	# find order, products
	order = Order.objects.filter(customer=request.user.customer).first() if user else None
	search = OrderProduct.objects.filter
	products = search(order=order) or search(session_order=request.session[cart_name])

	# order_quantity
	order_quantity = 0 if not 'order_quantity' in request.session else request.session['order_quantity']
	# request with data
	form = BillingInfoForm(request.POST or None)
	if form.is_valid():
		# creating an object but don't save it in the data base
		billing = form.save(commit=False)
		if user:
			billing.order = order
		else:
			billing.session_order = request.session[cart_name]
		billing.save()
		# creating a customer account if checkbox for account is checked
		# by creating a user, we create a customer by signal
		if billing.create_account and not user:
			username, password, last_name =  billing.first_name, billing.password, billing.last_name
			user = User.objects.create(username=username, password=password, first_name=username,
			last_name=last_name)
			user.login()
	total_price = sum([x.price for x in products])

		


	context = {
		'total':total_price,
		'form':form,
		'order_quantity':order_quantity,
		'products':products
	}
	return render(request, 'checkout.html', context)

def account(request):
	form = AccountForm(request.POST or None)

	if form.is_valid():
		username, password, email = form.data['username'], form.data['password'], form.data['email']
		user = authenticate(username=username, password=password, email=email)
		if user and request.path=='/login-page/':
			login(request, user)
		else:
			user = User.objects.create(username=username, email=email, password=password)
			login(request, user)
	title = '<p>Create an Account</p>' if request.path == '/register-page/' else '<p>Sing In</p>'

	context = {
		'title':title,
		'form':form
	}
	return render(request, 'account.html', locals())
	
