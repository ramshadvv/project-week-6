from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User
from django.db.models import Q
# Create your views here.
j=1
def user_login(request):
    if 'admin_id' in request.session:
        return redirect(home)

    if 'user_id' in request.session:
        return redirect(userprofile)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        if User.objects.filter(email=email):
            data = User.objects.get(email=email)
            if data.usertype == 'admin':
                user = authenticate(email=email,password=password)
                if user is not None :
                    request.session['admin_id']=email
                    login(request,user)
                    return redirect(home)
                else:
                    messages.error(request,'Invalid Entry')
                    return redirect(user_login)
            else:
                user = authenticate(email=email,password=password)
                if user is not None :
                    request.session['user_id']=email
                    login(request,user)
                    return redirect(userprofile)
                else:
                    messages.error(request,'Invalid Entry')
                    return redirect(user_login)
        else:
            messages.error(request,'Invalid Entry')
            return redirect(user_login)            
    return render(request, 'login.html')
def register(request):
    if 'user_id' in request.session:
        return redirect(userprofile)
    if request.method == 'POST':
        try:
            k=int(request.POST['phone'])
        except:
            messages.error(request,'Please enter the phone')
            return redirect(register)
        if request.POST.get('pass1') != request.POST.get('pass2'):
            messages.error(request,'Password is not match')
        elif len(request.POST['phone']) != 10:
            messages.error(request,'Please enter valid number')
        elif User.objects.filter(email = request.POST.get('email')) :
            messages.error(request,'Email already exists')
        elif User.objects.filter(phone = request.POST.get('phone')) :
            messages.error(request,'Phone number already exists')
        elif request.method == 'POST':
            f_name=request.POST.get('first_name')
            l_name= request.POST.get('last_name')
            dob =request.POST.get('birthday')
            gen = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('pass1')
            item = User.objects.create(
                email=email,
                first_name=f_name,
                last_name = l_name,
                birthday=dob,
                gender=gen,
                phone=phone,
            )
            item.set_password(password)
            item.save()
            messages.success(request, 'Registerd Successfully!!')
            return redirect(home)
    return render(request, 'signup.html')

def home(request):
    if 'admin_id' in request.session:
        if 'search' in request.GET:
            sh = request.GET['search']
            multiple_sh = Q(Q(first_name__icontains=sh) | Q(email__contains=sh))
            item = User.objects.filter(multiple_sh)
        else:
            item = User.objects.all()
        return render(request, 'index.html',{'data':item})

    if 'user_id' in request.session:
        return redirect(userprofile)

    return redirect(user_login)

# userprofile
def userprofile(request):
    if 'admin_id' in request.session:
        return redirect(home)   
    sess = request.session['user_id']
    item=User.object.get(email=sess)
    return render(request, 'profile.html',{'data' : item})

def useredit(request, uid):
    item=User.object.get(id=uid)
    if request.method == 'POST':
        try:
            k=int(request.POST['phone'])
        except:
            messages.error(request,'Please enter the phone')
            render(request, 'useredit.html',{'data' : item})
        if len(request.POST['phone']) != 10:
            messages.error(request,'Please enter valid number')
        elif item.email != request.POST.get('email'):
            if User.objects.filter(email = request.POST.get('email')) :
                messages.error(request,'Email already exists')
        elif item.phone != request.POST.get('phone'):
            if User.objects.filter(phone = request.POST.get('phone')) :
                messages.error(request,'Phone number already exists')
        elif request.method == 'POST':
            item.first_name = request.POST['first_name']
            item.last_name = request.POST['last_name']
            item.birthday = request.POST.get('birthday')
            item.gender = request.POST['gender']
            item.save()
            messages.success(request, 'Updated Successfully!!')
            return redirect(userprofile)
    return render(request, 'useredit.html',{'data' : item})


# edit

def edit(request, uid):
    item=User.object.get(id=uid)
    if request.method == 'POST':
        if len(request.POST['phone']) != 10:
            messages.error(request,'Please enter valid number')
        elif item.phone != request.POST.get('phone'):
            if User.objects.filter(phone = request.POST.get('phone')):
                messages.error(request,'Phone number already exists')
        elif item.email != request.POST.get('email'):
            if User.objects.filter(email = request.POST.get('email')) :
                messages.error(request,'Email already exists')
        elif request.method == 'POST':
            item.first_name = request.POST['first_name']
            item.last_name = request.POST['last_name']
            item.birthday = request.POST.get('birthday')
            item.gender = request.POST['gender']
            item.email = request.POST['email']
            item.phone = request.POST['phone']
            item.save()
            messages.success(request, 'Updated Successfully!!')
            return redirect(home)
        
    return render(request, 'edit.html',{'data' : item})

def user_logout(request):
    if 'admin_id' in request.session:
        request.session.flush()
        logout(request)
        return redirect(user_login)

    if 'user_id' in request.session:
        request.session.flush()
        logout(request)
        return redirect(user_login)
    return render(request,'login.html')
def delete(request,uid):
    item = User.objects.filter(id=uid).delete()
    messages.success(request, 'Deleted 1 record!!')
    return redirect(home)
