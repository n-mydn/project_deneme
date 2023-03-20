from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserAddProfile


class RegisterFrom(forms.Form):
    first_name = forms.CharField(max_length=30,label="Ad")
    last_name= forms.CharField(max_length=15, label="Soyad")
    email = forms.EmailField(label="E-Posta")
    username = forms.CharField(max_length=30,label="Kullanıcı Adı")
    password = forms.CharField(max_length=20,label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parola Doğrula",widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields= ["first_name","last_name","email","username","password","confirm"]

        def clean(self):
            first_name = self.cleaned_data.get("first_name")
            last_name = self.cleaned_data.get("last_name")
            email = self.cleaned_data.get("email")
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            confirm = self.cleaned_data.get("confirm")
            

            if password and confirm and password != confirm:
                raise forms.ValidationError('Parolalar Eşleşmiyor')
        
            values = {
                "password":password,
                "email":email,
                "last_name":last_name,
                "first_name":first_name,
                "username":username,
                }

            return values

class RegisterAddForm(ModelForm):
    class Meta:
        model = UserAddProfile
        fields = "__all__"


class AdminUserAddForm(ModelForm):
    class Meta:
        model = UserAddProfile
        fields = ["user_phone","user_department","user_role"]

class AdminUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola",widget=forms.PasswordInput)