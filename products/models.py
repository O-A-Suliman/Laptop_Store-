from django.db import models

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
    def __str__(self):
        return self.name
    
class StoreSetting(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    whatsapp_number=models.CharField(max_length=255)
    facebook_link=models.CharField(max_length=255)
    logo=models.ImageField(upload_to='products',null=True,blank=True)