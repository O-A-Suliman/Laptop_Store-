from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
from rest_framework import generics
from .serializers import ProductSerializer
# Create your views here.
class ProductsList(ListView):
    model=Product
    template_name="products/home.html"
    context_object_name="products"
    paginate_by=2
    def get_queryset(self):
        queryset= super().get_queryset()
        serech_queryset=self.request.GET.get("q")
        category_query=self.request.GET.get("category")
        if serech_queryset:
            queryset=queryset.filter(name__icontains=serech_queryset)
        if category_query:
            queryset=queryset.filter(category__name__icontains=category_query)
        return queryset
class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# دالة إرجاع منتج واحد بالتفصيل (لـ API)
class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer