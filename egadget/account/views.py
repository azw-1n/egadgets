from typing import Any
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import View,FormView,CreateView
from.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

# class HomeView(View):
#     def get(self,request):
#         form=LoginForm()
#         return render(request,'home.html',{'form':form})
class HomeView(FormView):
    template_name="home.html"
    form_class=LoginForm 

    def post(self,request,*args,**kwargs):
        form_data=LoginForm(data=request.POST)
        if form_data.is_valid():
            us=form_data.cleaned_data.get("username")
            pswd=form_data.cleaned_data.get("password")
            user=authenticate(request,username=us,password=pswd)
            print(user)
            if user:
                login(request,user)
                messages.success(request,"login Successfull!!")

                return redirect('custhome')
            else:
                messages.error(request,"sign in failed!!")
                return redirect('h')
        return render(request,"home.html",{"form":form_data})
    



class RegView(CreateView):
    template_name="reg.html"
    form_class=RegForm
    model=User
    success_url=reverse_lazy('h')

    def form_valid(self,form):
        messages.success(self.request,"Registration Successfull!!")
        return super().form_valid(form)
    
class lgutview(View):
    def get(self,request):
        logout(request)
        return redirect('h')
    
# class RegView(View):
#     def get(self,request):
#         form=RegForm
#         return render(request,"reg.html",{"form":form})
#     def post(self,request):
#         form_data=RegForm(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             messages.success(request,"Sign Up completed!")
#             return redirect("h")
#         return render(request,"reg.html",{"form":form_data})
