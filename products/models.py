from django.db import models
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
    product=models.ForeignKey(Product,related_name='orders',on_delete=models.CASCADE)
    date_order=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=Status.choices,default=Status.InProgress)
    def __str__(self):
        return self.name
