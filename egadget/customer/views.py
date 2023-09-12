from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,ListView,DetailView
from account.models import products,cart,order
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
#decorator
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please login first!!")
            return redirect("h")
    return inner 

decs=[never_cache,signin_required]


# Create your views here.

# class CustomerHomeView(View):
#     def get (self,request):
#         res=products.objects.all()

#         return render(request,"cust_home.html",{"data":res})
@method_decorator(decs,name="dispatch")
class CustomerHomeView(ListView):
    template_name="cust_home.html"
    queryset=products.objects.all()
    context_object_name="products"


# class ProductDetailView(View):
#     def get(self,request,**kwargs):
#         pid=kwargs.get('id')
#         pro=products.objects.get(id=pid)
#         return render(request,"product_details.html",{"data":pro})
@method_decorator(decs,name="dispatch")
    
class ProductDetailView(DetailView):
    template_name="product_details.html"
    pk_url_kwarg='id'
    queryset=products.objects.all()
    context_object_name='data'
decs
def addcart(request,*args,**kwargs):
    id=kwargs.get("id")
    pro=products.objects.get(id=id)
    user=request.user
    qty=request.POST.get('qnt')
    cart.objects.create(product=pro,user=user,quantity=qty)
    messages.success(request,"Added to Cart!")
    return redirect('custhome') 

@method_decorator(decs,name="dispatch")
class CartListView(ListView):
    template_name="cart.html"
    queryset=cart.objects.all()
    context_object_name="cart"

    def get_queryset(self):
        return cart.objects.filter(user=self.request.user,status='cart')
decs  
def removecart(request,**kwargs):
    pid=kwargs.get("id")
    c=cart.objects.get(id=pid)
    c.delete()
    messages.success(request,"Cart Item REmoved!!")
    return redirect('clist')

@method_decorator(decs,name="dispatch")
class PaymentView(TemplateView):
    template_name="payment.html"

    def post(self,request,*args,**kwargs):
        cid=kwargs.get("id")
        c=cart.objects.get(id=cid)
        ad=request.POST.get("address")
        ph=request.POST.get("phone")
        order.objects.create(cart=c,address=ad,phone=ph)
        c.status="Order placed"
        c.save()
        messages.success(request,"Order Placed Successfully!!")
        return redirect("clist")

@method_decorator(decs,name="dispatch")

class OrderListView(ListView):
    template_name="orders.html"
    queryset=order.objects.all()
    context_object_name="orders"

    def get_queryset(self):
        return order.objects.filter(cart__user=self.request.user)
    
decs
def cancelorder(request,*args,**kwargs):
    oid=kwargs.get("id")
    Order=order.objects.get(id=oid)
    Order.status='Cancelled'
    Order.save()
    messages.success(request,"Order Cancelled !!")
    return redirect('olist')
    

      

