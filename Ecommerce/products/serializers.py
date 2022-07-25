from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityVariant
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    quantity_type = QuantitySerializer()
    color_type = ColorSerializer()
    size_type = SizeSerializer()
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['id']

