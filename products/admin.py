from django.contrib import admin
from .models import Product,Category,StoreSetting
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
@admin.register(StoreSetting)
class AdminStoreSetting(admin.ModelAdmin):
    list_display=['name','whatsapp_number']