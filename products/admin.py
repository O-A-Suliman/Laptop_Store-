from django.contrib import admin
from .models import Product,Category,StoreSetting
# Register your models here.
@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display=["name","category","price","stack"]
    list_filter=['category',]
    fieldsets=(
        ('Basic data',{
            'fields':("name", "price", "description",'stack')
            }),
        ("Technical specifications",{
            'fields':('CPU','RAM','storage','GPU'),
        })
    )

admin.site.register(Category)
@admin.register(StoreSetting)
class AdminStoreSetting(admin.ModelAdmin):
    list_display=['name','whatsapp_number']