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
        serech_queryset=self.request.GET.get("q") #اي حاجة بعد ال q بتكون كلمة البحث
        category_query=self.request.GET.get("category") #بحث بناء على النوع
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
        context['orders_count']=Order.objects.filter(product=self.object).count()
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
    total=Order.objects.filter(status='COMPLETED').aggregate(total=Sum('total_price'))['total'] or 0
    return render(request,'products/dashboard_reports.html',{'total':total,"completed_order":completed_order})


def add_to_cart(request,product_id):
    cart=request.session.get('cart',{})
    product_id=str(product_id)
    product=get_object_or_404(Product,id=product_id)
    current_quantity_in_cart=cart.get(product_id,0)
    if current_quantity_in_cart + 1 > product.stock:
        messages.error(request, f"عذراً، لم يتبق سوى {product.stock} من هذا المنتج في المخزون.")
        return redirect("ProductsList") # نرجعه دون إضافة المنتج
    if product_id in cart:
        cart[product_id]+=1
    else:
        cart[product_id]=1
    request.session['cart']=cart
    request.session.modified = True
    messages.success(request, f"تم إضافة {product.name} إلى السلة بنجاح! 🛒")
    return redirect ("ProductsList")

def cart_view(request):
    cart=request.session.get('cart',{})
    products = Product.objects.filter(id__in=cart.keys())
    total_price=0
    cart_items=[]
    for product in products:
        product=get_object_or_404(Product,id=id)
        quantity=cart[str(product.id)]
        price=product.price
        subtotal=quantity*price
        cart_items.append({'product':product,"quantity":quantity,"subtotal":subtotal})
        total_price+=subtotal
    return render(request,'products/cart.html',{'cart_items':cart_items,'total_price':total_price})

def checkout_view(request):
    cart_items=[]
    total_price=0
    products = Product.objects.filter(id__in=cart.keys())
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = quantity * product.price
        cart_items.append({'product': product, "quantity": quantity, "subtotal": subtotal})
        total_price += subtotal
    cart = request.session.get('cart', {})
    if not cart:
        return redirect("ProductsList")
        
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # 1. تجهيز بداية رسالة الواتساب
        whatsapp_msg = f"مرحباً، أريد تأكيد طلب جديد 🛒:\n\n"
        whatsapp_msg += "تفاصيل المنتجات:\n"
        order = Order.objects.create(name=name, address=address, phone=phone, product=product)
        for product_id in cart:
            product = get_object_or_404(Product, id=int(product_id))
            quantity = cart[product_id]
            if quantity>=product.stock:
                messages.error(request, f"عذراً، الكمية المطلوبة من {product.name} غير متوفرة. المتاح فقط {product.stock}.")
                return redirect("cart_view") # نرجعه لصفحة السلة ليعدل الكمية
            price = product.price
            subtotal = quantity * price
            OrderItem.objects.create(
                order=order,      # <--- لاحظ كيف ربطناه بالفاتورة التي أنشأناها فوق
                product=product, 
                quantity=quantity, 
                total_price=subtotal
            )
        product.stock -= quantity
        product.save()
            
            # 2. إضافة اسم المنتج والكمية إلى رسالة الواتساب (داخل اللوب)            whatsapp_msg += f"- {product.name} (الكمية: {quantity})\n"
            
        # 3. إضافة بيانات العميل للرسالة (بعد انتهاء اللوب)
        whatsapp_msg += f"\n👤 بيانات العميل:\n"
        whatsapp_msg += f"الاسم: {name}\n"
        whatsapp_msg += f"الهاتف: {phone}\n"
        whatsapp_msg += f"العنوان: {address}\n"
        
        # تفريغ السلة
        del request.session['cart']
        
        # 4. جلب رقم الواتساب من الإعدادات وتوجيه العميل
        store_setting = StoreSetting.objects.first()
        if store_setting and store_setting.whatsapp_number:
            # تحويل النص العربي والمسافات إلى صيغة رابط (URL Encoding)
            encoded_msg = quote(whatsapp_msg)
            # إزالة علامة + من الرقم ليتوافق مع رابط واتساب
            wa_number = str(store_setting.whatsapp_number).replace('+', '')
            
            # الرابط النهائي
            whatsapp_url = f"https://wa.me/{wa_number}?text={encoded_msg}"
            return redirect(whatsapp_url)
        else:
            # في حال لم تكن قد أدخلت رقم واتساب في الداشبورد، نظهر له رسالة نجاح عادية
            messages.success(request, "🎉 تم استلام طلبك بنجاح! سنتواصل معك قريباً.")
            return redirect('ProductsList')
        
            
    return render(request, 'products/checkout.html', {
        'cart_items': cart_items, 
        'total_price': total_price
    })