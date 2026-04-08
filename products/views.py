from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Order,Category
from rest_framework import generics
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# Create your views here.
class ProductsList(ListView):
    model=Product
    template_name="products/home.html"
    context_object_name="products"
    paginate_by=2 #عدد المنتجات في كل صفحة
    #دالة البحث
    def get_queryset(self):
        queryset= super().get_queryset()
        serech_queryset=self.request.GET.get("q") #اي حاجة بعد ال q بتكون كلمة البحث
        category_query=self.request.GET.get("category") #بحث بناء على النوع
        if serech_queryset:
            queryset=queryset.filter(name__icontains=serech_queryset)
        if category_query:
            queryset=queryset.filter(category__name__icontains=category_query)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        return context
class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["related_products"]=Product.objects.filter(category=self.object.category).exclude(id=self.object.id)[:3]
        return context

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# دالة إرجاع منتج واحد بالتفصيل (لـ API)
class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@staff_member_required
def GetDashboard(request):
    pending_orders=Order.objects.filter(status='PENDING').count()
    total_products=Product.objects.count()
    completed_orders=Order.objects.filter(status='COMPLETED').count()
    low_stock=Product.objects.filter(stock__lt=3).count()
    latest_orders=Order.objects.filter(status__in=['PENDING', 'INPROGRESS']).order_by("-date_order")[:5]
    stats = {
    "pending_orders": pending_orders,
    "total_products": total_products,
    "completed_orders": completed_orders,
    "low_stock": low_stock,
    "latest_orders":latest_orders
}
    return render(request,'products/dashboard_home.html',stats)

@staff_member_required
def dashboard_orders_view(request):
    orders=Order.objects.all().order_by("-date_order")
    return render(request,'products/dashboard_orders.html',{"orders":orders})

@staff_member_required
def complete_order_view(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    order.status="COMPLETED"
    order.save()
    return redirect("dashboard_orders")

@method_decorator(staff_member_required, name='dispatch')
class DashboardInventoryView(ListView):
    model=Product
    template_name='products/dashboard_inventory.html' 
    context_object_name="products"
    def get_queryset(self):
        queryset= super().get_queryset()
        serech_queryset=self.request.GET.get("q")
        category_query=self.request.GET.get("category")
        if serech_queryset:
            queryset=queryset.filter(name__icontains=serech_queryset)
        if category_query:
            queryset=queryset.filter(category__name__icontains=category_query)
        return queryset
    
@staff_member_required
def dashboard_reports_view(request):
    completed_order=Order.objects.filter(status='COMPLETED').count()
# aggregate() بترجع Dictionary مش رقم
# بنستخدم alias (total=) عشان نسمي النتيجة باسم واضح
# ['total'] عشان نطلع الرقم من القاموس مباشرة
    total=Order.objects.filter(status='COMPLETED').aggregate(total=Sum('product__price'))['total']
    return render(request,'products/dashboard_reports.html',{'total':total,"completed_order":completed_order})


def add_to_cart(request,product_id):
    cart=request.session.get('cart',{})
    product_id=str(product_id)
    if product_id in cart:
        cart[product_id]+=1
    else:
        cart[product_id]=1
    request.session['cart']=cart
    request.session.modified = True
    return redirect ("ProductsList")

def cart_view(request):
    cart=request.session.get('cart',{})
    total_price=0
    cart_items=[]
    for product_id in cart:
        product=get_object_or_404(Product,id=int(product_id))
        quantity=cart[product_id]
        price=product.price
        subtotal=quantity*price
        cart_items.append({'product':product,"quantity":quantity,"subtotal":subtotal})
        total_price+=subtotal
    return render(request,'products/cart.html',{'cart_items':cart_items,'total_price':total_price})

def checkout_view(request):
    cart=request.session.get('cart',{})
    if not cart:
        return redirect("ProductsList")
    if request.method=='POST':
        total_price=0
        for product_id in cart:
            product=get_object_or_404(Product,id=int(product_id))
            quantity=cart[product_id]
            price=product.price
            subtotal=quantity*price
            total_price+=subtotal
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        order=Order.objects.create(name=name,address=address,phone=phone,total_price=total_price)
        order.save()
        del request.session['cart']
        return redirect('ProductsList')
    return render('products/checkout.html')