from rest_framework import serializers
from core.models import (ClotheProduct,
					AccessorieProduct, CosmeticProduct,
					Category, Image)



class ClotheProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClotheProduct
        fields = '__all__'

class AccessorieProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessorieProduct
        fields = '__all__'

class CosmeticProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CosmeticProduct
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

list_serializers = [
    ClotheProductSerializer, AccessorieProductSerializer,
    CosmeticProductSerializer, CategorySerializer
]
