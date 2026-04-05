from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
# Create your views here.
class ProductsList(ListView):
    model=Product
    template_name="products/home.html"
    context_object_name="products"
    def get_queryset(self):
        queryset= super().get_queryset()
        serech_queryset=self.request.GET.get("p")
        if serech_queryset:
            queryset=queryset.objects.filter(name__icontains=serech_queryset)
        return queryset
class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"