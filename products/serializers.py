from rest_framework import serializers
from .models import Product, Category

# مترجم الأقسام
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# مترجم المنتجات
class ProductSerializer(serializers.ModelSerializer):
    # استخدمنا مترجم الأقسام هنا لكي تظهر بيانات القسم كاملة داخل المنتج بدلاً من مجرد رقمه (ID)
    category = CategorySerializer(read_only=True) 

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category']