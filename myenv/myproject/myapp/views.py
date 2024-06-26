from django.shortcuts import render, redirect
from .models import *
import random
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.conf import settings


def index(request):
    try:
        user = User.objects.get(email=request.session['email'])
        if user.usertype=="buyer":
            return render(request,"index.html")
        else:
            return render(request,"sindex.html")

    except:
        return redirect("login") 
    




def contact(request):
    user = User.objects.get(email=request.session['email'])
    if request.method=="POST":
        if user.usertype=="buyer":
            return render(request,'contact.html')
        else:
            return render(request,'scontact.html')
    else:
        if user.usertype=="buyer":
            return render(request,'contact.html')
        else:
            return render(request,'scontact.html')
    

def about(request):
    user = User.objects.get(email = request.session['email']) 
    if user.usertype=="buyer":
        return render(request, 'about.html')
    else:
        return render(request, 'sabout.html')



def news(request):
    return render(request, 'news.html')

def signin(request):
    if request.method == "POST":
        
        try:
            msg = "Email already Exist.Try with other Email!!!"
            user = User.objects.get(email = request.POST['email']) 
            return render(request, 'login.html', {'msg': msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                
                User.objects.create(
                usertype = request.POST['usertype'],
                email = request.POST['email'],
                password = request.POST['password'],
                name = request.POST['name'],
                mobile = request.POST['mobile'],
                age = int(request.POST['age']),
                profile = request.FILES['profile'],
                )
                msg = "Signin sucessfully!!!"
                return render(request, 'login.html', {'msg': msg})
            else:
                msg = "Password does not match!!!"
                return render(request, 'signin.html', {'msg': msg})
           
    else:
        return render(request, 'signin.html')
            

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            if user.password==request.POST['password']: 
                request.session['email'] = user.email
                request.session['profile'] = user.profile.url
                if user.usertype=="buyer":
                    return render(request, 'index.html')
                else:
                   return render(request, 'sindex.html') 
                
            else:
                msg = "Email and Password does not match"
                return render(request, 'login.html', {'msg': msg})
        except:
            msg = "Email is not Registered"
            return render(request, 'login.html', {'msg': msg})
            
    else:
        return render(request, 'login.html')
        

def logout(request):
    del request.session['email']
    del request.session['profile']
    return render(request,'login.html')


def cpass(request):
    user = User.objects.get(email = request.session['email'])
    if request.method == "POST":
        
        if user.password == request.POST['opass']:
            if request.POST['npassword']==request.POST['rpassword']:
                user.password=request.POST['npassword']
                user.save()
                msg = "password updated successfully"
                if user.usertype == "buyer":
                    return render(request,'index.html',{'msg': msg})
                else:
                    return render(request,'sindex.html',{'msg': msg})
                    
            else:
                msg = "New Password and Confirm New Password do not match"
                if user.usertype == "buyer":
                
                    return render(request, 'cpass.html', {'msg': msg})
                else:
                    return render(request, 'scpass.html', {'msg': msg})
               
        else:
            msg = "Old Password is incorrect"
            if user.usertype == "buyer":
                return render(request, 'cpass.html', {'msg': msg})
            else:
                return render(request, 'scpass.html', {'msg': msg})
    else:
        if user.usertype == "buyer":
            return render(request, 'cpass.html')
        else:
            return render(request, 'scpass.html')
        

def fpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(mobile=request.POST['mobile'])
            mobile = request.POST['mobile']
            otp = random.randint(1001, 9999)
        
      

            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"yLFsRAMHrhb7tpkZq6uIvzQaWg8imVEd0Oo4xGNU5YfXcC1weTyxh6DHAuQXngIlwf8PWKOtqjZs9VLT","variables_values":str(otp),"route":"otp","numbers":mobile}

            headers = {
                'cache-control': "no-cache"
            }

            response = request.request("GET", url, headers=headers, params=querystring)

            print(response.text)
            request.session['mobile']=user.mobile
            request.session['otp']=otp
            return render(request, 'otp.html')
        except:
            msg = "mobile number Does not Exist"
            return render(request, 'fpass.html', {'msg': msg})

    else:    
       return render(request, 'fpass.html')
  
  
def otp(request):
    otp = request.session['otp']
    uotp = int(request.POST['uotp'])
    try:
        if otp == uotp:
            del request.session['otp']
            return render(request,'newpassword.html')
        else:
            msg = "Invalid OTP"
            return render(request,'otp.html',{'msg': msg})
    except:
        pass
    
    
def newpassword(request):
    if request.method=="POST":
        user = user.objects.get(mobile = request.session['mobile'])
        
        if request.POST['npassword']==request.POST['cpassword']:
            user.password=request.POST['npassword']
            user.save()
            msg = "Password updated successfully"
            return render(request,'login.html',{'msg':msg})
        else:
            msg = "New password and confirm password does not match"
            if user.usertype=="buyer":
                return render(request,'newpasssword.html',{'msg':msg})
            else:
                return render(request,'snewpasssword.html',{'msg':msg})
    else:
        return render(request,'newpasssword.html')

def uprofile(request):
    user = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        user.name = request.POST['name']
        user.mobile = request.POST['mobile']
        user.age = request.POST['age']
        try:
            user.profile = request.FILES['profile']
            user.save()
        except:
           pass
        request.session['profile'] = user.profile.url
        user.save()
        if user.usertype=="buyer":
            return render(request,'index.html',{'user': user})
        else:
            return render(request,'sindex.html',{'user': user})
        
    
    else:
        if user.usertype=="buyer":
            return render(request, 'uprofile.html',{'user': user})
        else:
            return render(request, 'sprofile.html',{'user': user})

def sindex(request):
    return render(request, 'sindex.html')

def sprofile(request):
    return render(request, 'sprofile.html')

def scpass(request):
    return render(request, 'scpass.html')

def scontact(request):
    return render(request, 'scontact.html')

def sabout(request):
    return render(request, 'sabout.html')

def snewpassword(request):
    return render(request, 'snewpassword.html')

def sadd(request):
    user = User.objects.get(email = request.session['email'])
   
    if request.method=="POST":
        try:
            Product.objects.create(
                user = user,
                pcategory = request.POST['pcategory'],
                pprice = request.POST['pprice'],
                pdec = request.POST['pdec'],
                pname = request.POST['pname'],
                pimage = request.FILES['pimage']
        
            )
            msg = "Product added sucessfully"
            return render(request, 'sindex.html',{'msg':msg})  
        except:
            msg = "you might be missing Something"
            return render(request, 'sadd.html', {'msg': msg}) 
    else:
         return render(request, 'sadd.html')
        
def sview(request):
    user = User.objects.get(email= request.session ['email'])
    product = Product.objects.filter(user=user)
    return render(request, 'sview.html',{'product':product})

def pdetails(request,pk):
    user = User.objects.get(email= request.session ['email'])
    product = Product.objects.get(pk=pk)
    return render(request,'pdetails.html',{'product': product})

def edit(request,pk):
    user = User.objects.get(email= request.session['email'])
    product = Product.objects.get(pk=pk)
    if request.method=="POST":
        product.pcategory = request.POST['pcategory']
        product.pname = request.POST['pname']
        product.pprice= request.POST['pprice']
        product.pdec = request.POST['pdec']
        try:
            product.pimage = request.FILES['pimage']
            product.save()
        except:
            pass
        request.session['pimage'] = product.pimage.url
        product.save()
        msg = "Product updated succesfully"
        return render(request,'sindex.html',{'msg': msg})
        
    else:
         return render(request,'edit.html',{'product': product})   
     
def pdelete(request,pk):
    user = User.objects.get(email= request.session['email'])
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('sindex')

def shop(request):
    user = User.objects.get(email= request.session['email'])
    product = Product.objects.all()
  
    return render(request, 'shop.html',{'product': product })

def bdetails(request,pk):
    user = User.objects.get(email= request.session ['email'])
    product = Product.objects.get(pk=pk)
    return render(request,'bdetails.html',{'product': product})

def addwish(request,pk):
    user = User.objects.get(email= request.session ['email'])
    product = Product.objects.get(pk=pk)
    Wishlist.objects.create(user=user,product=product)
    return redirect('wishlist')

def wishlist(request):
    user = User.objects.get(email= request.session ['email'])
    wishlist = Wishlist.objects.filter(user=user)
    return render(request,'wishlist.html',{'wishlist': wishlist})



def wishdelete(request,pk):
    user = User.objects.get(email= request.session ['email'])
    wishlist = Wishlist.objects.filter(user=user,pk=pk)
    wishlist.delete()
    return redirect('wishlist')



def addcart(request,pk):
     try:
        user = User.objects.get(email = request.session['email'])
        product = Product.objects.get(pk=pk)
        Cart.objects.create(user=user,product=product,tprice=product.pprice,
                            cqty =1,
                            cprice=product.pprice,
                            payment = False)
        return redirect ('cart')
     except:
         return redirect("login")
     
     
def cart(request):
    user = User.objects.get(email = request.session['email'])
    cart = Cart.objects.filter(user=user,payment=False)
    net = 0
   
    for i in cart:
        net+=i.tprice

    if net>=20000:
        ship = 0

    else:
        ship=100

    sc = net+ship
    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': sc * 100, 'currency': 'INR', 'payment_capture': 1})
    
    context = {
                    'payment': payment,
                    #'book':book,  # Ensure the amount is in paise
                }


   
    return render (request,'cart.html',{'cart':cart,'net':net,'ship':ship,'sc':sc,'context':context})


def cartdelete(request,pk):
    user = User.objects.get(email = request.session['email'])
    cart = Cart.objects.filter(user=user,pk=pk)
    cart.delete()
    return redirect ('cart')


def changeqty(request,pk):
    c = Cart.objects.get(pk=pk)
    print(c)
    c.cqty = int(request.POST['cqty'])
    c.save()
    c.tprice = c.cprice*c.cqty
    print(c.tprice)
    c.save()
    return redirect("cart")

def sucess(request):
    try:
        print(request.session['email'])
        user = User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user)
        for i in cart:
            i.payment=True
            i.save()
        return render(request,'sucess.html',{'cart':cart})
    
    except Exception as e:
        print(e)
        return render(request,'index.html')
    
def myorder(request):
    user = User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user,payment=True)
    return render(request,'myorder.html',{'cart':cart})
