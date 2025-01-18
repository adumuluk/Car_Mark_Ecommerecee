from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Sell.models import Product,Cart,Order
from django.db.models import Q
import random

# Create your views here.
def testing(request):
    return HttpResponse("linked suceessfully")

def home(request):
   #userid=request.user.id
   #print(userid)
   #print("result:",request.user.is_authenticated)
   #return render(request,"index.html")
   context={}
   p=Product.objects.filter(is_active=True)
   print(p)
   context['product']=p
   return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['product']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'

    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    #print(min)
    #print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    print(p)
    context={}
    context['product']=p
    return render(request,'index.html',context)

def pdetails(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,"product_details.html",context)

def cart(request):
    return render(request,"cart.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="" :
            context['errormsg']="field cannot be empty"
            return render(request,'register.html',context)
        else :
            try:
                u=User.objects.create(username=uname,password=upass)
                u.set_password(upass)
                u.save()
                context["success"]="user created successfully pls login "
                return render(request,'register.html',context)
            except Exception:
                context['errormsg']="username already exist"
                return render(request,'register.html',context)

    else:
        return render(request,"register.html")

def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="" :
            context['errormsg']="field cannot be empty"
            return render(request,'login.html',context)
            return HttpResponse('Data is fetch')
        else :
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                 context['errormsg']="invalid & password"
                 return render(request,'login.html',context)
                 
            #print(u)
            return HttpResponse("in else part")
                
    else :
            return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect ('/home')            

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect ('/viewcart')

def viewcart(request):
    userid=request.user.id 
    c=Cart.objects.filter(uid=userid) 
    s=0
    np=len(c)
    for x in c:
        s=s+x.pid.price *x.qty
    context={}
    context['n']=np
    context['products']=c
    context['total']=s 
    return render(request,'cart.html',context)
'''
def makepayment(request):
   
    client = razorpay.Client(auth=("rzp_test_VyAPazEIwwyaNA", "vVdcwXIJZt8HmcgVBRhpEiKy"))

    data = { "amount": 2000, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    return HttpResponse("success")
'''
def addtocart(request,pid):
    if request.user.is_authenticated:
            userid=request.user.id
            u=User.objects.filter(id=userid)
            print(u[0])
            p=Product.objects.filter(id=pid)
            print(p[0])
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
        # print(userid)
        # print(pid)
            return redirect("/viewcart")   
    else:
        return redirect("/user_login")

def  updateqty(request,qv,cid):
    #print(type(qv))
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print('order id is:-',oid)
    #print(c)

    for x in c:
        #print(x)
        #print(x.pid)
        #print(x.uid)
        #print(x.qty)

        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()

    orders=Order.objects.filter(uid=request.user.id)

    s=0
    np=len(c)
    context={} 
    for x in c:
                 
        s=s+x.pid.price *x.qty                           
        context={}
        context['n']=np
        context['products']=c
        context['total']=s
    return render(request,"placeorder.html",context)