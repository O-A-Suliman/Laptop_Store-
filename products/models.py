from django.db import models
from django.core.cache import cache
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=255)
    category=models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE)
    description=models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products',null=True,blank=True)
    CPU=models.CharField(max_length=255)
    RAM=models.CharField(max_length=255)
    storage=models.CharField(max_length=255)
    GPU=models.CharField(max_length=255)
    stock=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class StoreSetting(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    whatsapp_number=PhoneNumberField()
    facebook_link=models.CharField(max_length=255)
    logo=models.ImageField(upload_to='products',null=True,blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # نقوم بالحفظ العادي أولاً
        cache.delete('site_settings_cache')
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class Status(models.TextChoices):
        Pending='PENDING',"Pending"
        InProgress='INPROGRESS','In Progress'
        Completed='COMPLETED','Completed'
        Cancelled='CANCELLED','Cancelled'
    name=models.CharField(max_length=255)
    phone=PhoneNumberField()
    date_order=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=Status.choices,default=Status.InProgress)
    address=models.CharField(max_length=255,blank=True,null=True)
    grand_total=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    def __str__(self):
        return self.name
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product,related_name='orders',on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    quantity=models.IntegerField(default=0)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    def __str__(self):
        return self.product.name
