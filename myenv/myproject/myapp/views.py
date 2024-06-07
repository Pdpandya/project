from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User
import random
import requests

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def news(request):
    return render(request, 'news.html')

def shop(request):
    return render(request, 'shop.html')

def signin(request):
    if request.method == "POST":
        
        try:
            user = User.objects.get(email = request.POST['email']) 
            msg = "Email already Exist.Try with other Email!!!"
            return render(request, 'login.html', {'msg': msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                
                User.objects.create(
                    email = request.POST.get('email'),
                    password = request.POST.get('password'),
                    name = request.POST.get('name'),
                    mobile = request.POST.get('mobile'),
                    age = int(request.POST.get('age')),
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
                return render(request,'index.html')
                
            else:
                msg = "Email and Password do not match"
                return render(request, 'login.html', {'msg': msg})
        except:
            msg = "Email is not Registered"
            return render(request, 'login.html', {'msg': msg})
            
    else:
        return render(request, 'login.html')
        

def logout(request):
    del request.session['email']
    return render(request,'login.html')


def cpass(request):
    if request.method == "POST":
        user = User.objects.get(email = request.session['email'])
        if user.password == request.POST['opass']:
            if request.POST['npassword']==request.POST['rpassword']:
                user.password=request.POST['npassword']
                user.save()
                msg = "password updated successfully"
                return render(request,'index.html',{'msg': msg})
       
            else:
                msg = "New Password and Confirm New Password do not match"
                return render(request, 'cpass.html', {'msg': msg})
        else:
            msg = "Old Password is incorrect"
            return render(request, 'cpass.html', {'msg': msg})
    else:
        return render(request, 'cpass.html')

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

            response = requests.request("GET", url, headers=headers, params=querystring)

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
            return render(request,'newpasssword.html',{'msg':msg})
    else:
        return render(request,'newpasssword.html')


def profile(request):
    return render(request,'profile.html')