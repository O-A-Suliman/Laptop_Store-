from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Order,Category,StoreSetting,OrderItem
from rest_framework import generics
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from urllib.parse import quote
# Create your views here.
class ProductsList(ListView):
    model=Product
    template_name="products/home.html"
    context_object_name="products"
    paginate_by=5 #عدد المنتجات في كل صفحة
    #دالة البحث
    def get_queryset(self):
        queryset= super().get_queryset()
        serech_queryset=self.request.GET.get("q")
        category_query=self.request.GET.get("category") 
        if serech_queryset:
            queryset=queryset.filter(name__icontains=serech_queryset)
        if category_query:
            queryset=queryset.filter(category__name__icontains=category_query)
        queryset=queryset.select_related('category')
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
        context['orders_count'] = OrderItem.objects.filter(product=self.object).count()
        return context

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
    total=Order.objects.filter(status='COMPLETED').aggregate(total=Sum('grand_total'))['total'] or 0
    return render(request,'products/dashboard_reports.html',{'total':total,"completed_order":completed_order})


def add_to_cart(request,product_id):
    cart=request.session.get('cart',{})
    product_id=str(product_id)
    product=get_object_or_404(Product,id=product_id)
    current_quantity_in_cart=cart.get(product_id,0)
    if current_quantity_in_cart + 1 > product.stock:
        messages.error(request, f"Sorry, only {product.stock} of this product left in stock.")
        return redirect("ProductsList")
    if product_id in cart:
        cart[product_id]+=1
    else:
        cart[product_id]=1
    request.session['cart']=cart
    request.session.modified = True
    messages.success(request, f"{product.name} was successfully added to the cart! 🛒")
    return redirect ("ProductsList")

def cart_view(request):
    cart=request.session.get('cart',{})
    products = Product.objects.filter(id__in=cart.keys())
    total_price=0
    cart_items=[]
    for product in products:
        quantity=cart[str(product.id)]
        price=product.price
        subtotal=quantity*price
        cart_items.append({'product':product,"quantity":quantity,"subtotal":subtotal})
        total_price+=subtotal
    return render(request,'products/cart.html',{'cart_items':cart_items,'total_price':total_price})

def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect("ProductsList")

    cart_items = []
    total_price = 0
    products = Product.objects.filter(id__in=cart.keys())
    
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        cart_items.append({'product': product, "quantity": quantity, "subtotal": subtotal})
        total_price += subtotal
        
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        whatsapp_msg = f"Hello, I would like to confirm a new order 🛒:\n\nProduct Details:\n"
        
        order = Order.objects.create(
            name=name, 
            address=address, 
            phone=phone,
            grand_total=total_price 
        )
        
        for product in products: 
            quantity = cart[str(product.id)]
            
            if quantity > product.stock:
                messages.error(request, f"Sorry, the requested quantity for {product.name} is unavailable. Only {product.stock} left.")
                return redirect("cart_view")
                
            subtotal = quantity * product.price
            
            OrderItem.objects.create(
                order=order,      
                product=product, 
                quantity=quantity, 
                total_price=subtotal
            )
            
            product.stock -= quantity
            product.save()
            
            whatsapp_msg += f"- {product.name} (Quantity: {quantity})\n"
            
        whatsapp_msg += f"\n👤 Customer Details:\nName: {name}\nPhone: {phone}\nAddress: {address}\n"
        
        del request.session['cart']
        
        store_setting = StoreSetting.objects.first()
        if store_setting and store_setting.whatsapp_number:
            encoded_msg = quote(whatsapp_msg)
            wa_number = str(store_setting.whatsapp_number).replace('+', '')
            whatsapp_url = f"https://wa.me/{wa_number}?text={encoded_msg}"
            return redirect(whatsapp_url)
        else:
            messages.success(request, "🎉 Your order has been received successfully! We will contact you soon.")
            return redirect('ProductsList')
            
    return render(request, 'products/checkout.html', {
        'cart_items': cart_items, 
        'total_price': total_price
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Product removed from cart successfully! 🗑️")
        
    return redirect("cart_view")