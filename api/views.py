from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import list_serializers
from core.models import (Product, ClotheProduct,
					AccessorieProduct, CosmeticProduct,
					Category, Image)

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
	info = {
		'api_url':{
			'list':'(class_product --> put the class product here)-list/',
			'item-details':'/klass_product/id/'
		},
		'class_products':[
			'CloseProduct',
			'AccessorieProduct',
			'CosmeticProduct'
		]

	}
	return Response(info)


# dynamic in getting and dealing with data in order to make this available
@api_view(['GET'])
def product_list(request, klass_prdt):
	# return the list product of a category-->klass_prdt
	queryset = Product.all_products(ClotheProduct, AccessorieProduct,
	CosmeticProduct, Category)
	products = [prdt for prdt in queryset if type(prdt).__name__ == klass_prdt]
	try:
		klassSerializer = [klassS for klassS in list_serializers if klassS.Meta.model.__name__ == klass_prdt][0]
	except IndexError:
		raise Http404()

	serializer = klassSerializer(products, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, klass_prdt, pk):
	klassSerializer = [klassS for klassS in list_serializers if klassS.Meta.model.__name__ == klass_prdt][0]
	product = (klassSerializer.Meta.model).objects.filter(product=pk)
	serializer = klassSerializer(product)
	return Response(serializer.data)
 