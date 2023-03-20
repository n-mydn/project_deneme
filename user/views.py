from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from .models import UserAddProfile
# Create your views here.


def login(request):
    form = LoginForm(request.POST or None)
    context={
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)
        
        messages.success(request,"Başarıyla Giriş Yaptınız.")
        auth_login(request,user)

        user_add = UserAddProfile.objects.get(user=request.user.id)
        
        if user_add.user_role.name == "Hastane Admini":
            return redirect("feedback:admin_all_feedback")
            
        if user_add.user_role.name == "Departman Admini":
            return redirect("feedback:d_admin_index") 
      
        return redirect("index")
            
    return render(request,"login.html",context)

"""
def d_login(request):
    form = LoginForm(request.POST or None)
    context={"form":form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user=authenticate(username=username,password=password)
        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola hatalı")
            return render(request,"d_login.html",context)
        messages.success(request,"Başarıyla Giriş Yaptınız...")
        auth_login(request,user)
        return redirect("feedback:d_admin_index")
    return render(request,"department_admin/login.html",context)

def a_login(request):
    form = LoginForm(request.POST or None)
    context={"form":form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user=authenticate(username=username,password=password)
        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola hatalı")
            return render(request,"d_login.html",context)
        messages.success(request,"Başarıyla Giriş Yaptınız...")
        auth_login(request,user)

        if request.user.username == "admin":
            return redirect("feedback:admin_all_department")
        elif request.user.username == "acil_servis_admin":
            return redirect("feedback:d_admin_index")
            
    return render(request,"admin/login.html",context)
"""

def logout(request):
    auth_logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız.")
    return redirect("index")