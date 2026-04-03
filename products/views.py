from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
# Create your views here.
class ProductsList(ListView):
    model=Product
    template_name="products/home.html"
    context_object_name="products"

class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"