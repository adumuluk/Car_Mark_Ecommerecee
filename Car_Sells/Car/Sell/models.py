from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    cat=((1,'Small SUV'),(2,'Medium SUV'),(3,'Large SUV'))
    name=models.CharField(max_length=40,verbose_name=" product name")
    price=models.FloatField()
    details=models.CharField(max_length=10000,verbose_name="product details")
    cat=models.IntegerField(verbose_name="category",choices=cat)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name
class Cart(models.Model):
        uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
        pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")     
        qty=models.IntegerField(default=1)    

class Order(models.Model):
    order_id=models.CharField(max_length=100)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid") 
    qty=models.IntegerField(default=1)

