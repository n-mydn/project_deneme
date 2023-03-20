from django.db import models
from django.contrib.auth.models import User
from feedback.models import Department,Company,Country,City
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

userroles_choice = (
    ("Admin","Admin"),
    ("Hastane Admini","Hastane Admini"),
    ("Departman Admini","Departman Admini"),
    ("Departman Kullanıcısı","Departman Kullanıcısı"),
    ("Personel","Personel"),
    ("Hasta","Hasta"),
)

user_status_choice=(
    ("Aktif","Aktif"),
    ("Pasif","Pasif"),
)

class UserRoles(models.Model):
    name = models.CharField(max_length=21,verbose_name="user_roles",choices=userroles_choice)
    
    def __str__(self):
        return self.name

class UserAddProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="Kullancı Adı")
    user_company = models.ForeignKey(Company,verbose_name="Hastane",on_delete=models.CASCADE)
    user_role = models.ForeignKey(UserRoles,verbose_name="Rol",on_delete=models.CASCADE)
    user_department = models.ForeignKey(Department,verbose_name="Departman",on_delete=models.CASCADE)
    user_phone = PhoneNumberField(verbose_name="Telefon Numarası")
    user_country = models.ForeignKey(Country,verbose_name="Ülke",on_delete=models.CASCADE)
    user_city = models.ForeignKey(City,verbose_name="Şehir",on_delete=models.CASCADE)
    user_adress = models.TextField(max_length=100,verbose_name="Adres",blank=True,null=True)
    user_status = models.CharField(max_length=5,choices=user_status_choice,verbose_name="Statü")

    def __str__(self):
        return self.user.username