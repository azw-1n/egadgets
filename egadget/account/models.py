from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class products(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to='product_images')
    description=models.CharField(max_length=500)
    options=(
        ('mobile phone','mobile phone'),
        ('earphone','earphone'),
        ('laptop','laptop'),
        ('tablet','tablet'),
        ('smart watch','smart watch'),
        ('BT speaker','BT speaker')
    )
    category=models.CharField(max_length=200,choices=options,default='mobile phone')

class cart(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=100,default='cart')

    @property
    def totalamnt(self):
        return self.product.price*self.quantity





class order(models.Model):
    cart=models.OneToOneField(cart,on_delete=models.CASCADE,related_name='cartorder')
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=500,null=True)
    phone=models.IntegerField(null=True)
    options=(
        ('Order placed','Order placed'),
        ('Shipped','Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    status=models.CharField(max_length=100,choices=options,default='Order placed')
  