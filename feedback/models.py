from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

country_choices=(
    ("Türkiye","Türkiye"),
    ("Almanya","Almanya"),
    ("Amerika Birleşik Devletleri","Amerika Birleşik Devletleri"),
    ("Arjantin","Arjantin"),
    ("Azerbaycan","Azerbaycan"),
    ("Brezilya","Brezilya"),
    ("Bulgaristan","Bulgaristan"),
    ("Danimarka","Danimarka"),
    ("Fransa","Fransa"),
    ("Gürcistan","Gürcistan"),
    ("Hollanda","Hollanda"),
    ("Irak","Irak"),
    ("İngiltere","İngiltere"),
    ("İran","İran"),
    ("İspanya","İspanya"),
    ("İtalya","İtalya"),
    ("Uruguay","Uruguay"),
)

city_choices=(
    ("İstanbul(Anadolu)","İstanbul(Anadolu)"),
    ("İstanbul(Avrupa)","İstanbul(Avrupa)"),
    ("Ankara","Ankara"),
    ("Bursa","Bursa"),
    ("İzmir","İzmir"),
    ("Adana","Adana"),
    ("Adıyaman","Adıyaman"),
    ("Afyonkarahisar","Afyonkarahisar"),
    ("Ağrı","Ağrı"),
    ("Aksaray","Aksaray"),
)

status_choices=(
    ("Aktif","Aktif"),
    ("Pasif","Pasif"),
)

dprt_choice= (
    ("Acil Servis", "Acil Servis"),
    ("Algoloji", "Algoloji"),
    ("Aile Hekimliği" , "Aile Hekimliği"),
    ("Amatem","Amatem(Alkol ve Madde Bağımlığı)"),
    ("Anesteziyoloji ve Reanimasyon","Anesteziyoloji ve Reanimasyon"),
    ("Beyin ve Sinir Cerrahisi","Beyin ve Sinir Cerrahisi"),
    ("Cerrahi Onkolojisi","Cerrahi Onkolojisi"),
    ("Çocuk Bölümü","Çocuk Bölümü"),
    ("Çocuk Diş Hekimliği","Çocuk Diş Hekimliği"),
    ("Cildiye","Deri ve Zührevi Hastalıkları"),
    ("Diş Hekimliği","Diş Hekimliği"),
    ("Endodonti","Endodonti"),
    ("Endokrin","Endokrinoloji ve Metabolizma Hastalıkları"),
    ("Enfeksiyon","Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji"),
    ("Fiziksel Tıp ve Rehabilitasyon","Fiziksel Tıp ve Rehabilitasyon"),
    ("Gastroenteroloji","Gastroenteroloji"),
    ("Gelişimsel Pediatri","Gelişimsel Pediatri"),
    ("Genel Cerrahi","Genel Cerrahi"),
    ("Geriatri","Geriatri"),
    ("Göğüs Cerrahisi","Göğüs Cerrahisi"),
    ("Göz Hastalıkları","Göz Hastalıkları"),
    ("Hematoloji","Hematoloji"),
    ("İç Hastalıkları(Dahiliye)", "İç Hastalıkları(Dahiliye)"),
    ("İmmünoloji ve Alerji Hastalıkları","İmmünoloji ve Alerji Hastalıkları"),
    ("İş ve Mesleki Hastalıkları","İş ve Mesleki Hastalıkları"),
    ("Kadın Hastalıkları ve Doğum","Kadın Hastalıkları ve Doğum"),
    ("Kalp ve Damar Cerrahisi","Kalp ve Damar Cerrahisi"),
    ("Kulak Burun Boğaz Hastalıkları","Kulak Burun Boğaz Hastalıkları"),
    ("Nefroloji","Nefroloji"),
    ("Nöroloji","Nöroloji"),
    ("Ordodonti","Ordodonti"),
    ("Perinatoloji","Perinatoloji"),
    ("Plastik Rekonstrüktif Estetik Cerrahi","Plastik Rekonstrüktif Estetik Cerrahi"),
    ("Ruh Sağlığı ve Hastalıkları(Psikiyatri)","Ruh Sağlığı ve Hastalıkları(Psikiyatri)"),
    ("Üroloji","Üroloji"),
    ("Radyoloji","Radyoloji"),
    ("*****","*****"),
) 

type_choice =(
    ("Öneri","Öneri"),
    ("Şikayet","Şikayet"),
    ("Teşekkür","Teşekkür"),
)

reason_choice=(
    ("Kötü Davranış","Kötü Davranış"),
    ("Hijyen Azlığı","Hijyen Azlığı"),
    ("Personelin Tutum ve Davranışı","Personelin Tutum ve Davranışı"),
    ("Personel Azlığı","Personel Azlığı"),
    ("Refakatçi İmkanı","Refaketçi İmkanı"),
    ("Hastane Olanakları","Hastane Olanakları"),
    ("Diğer","Diğer"),
)

source_choice=(
    ("Personel","Personel"),
    ("Hijyen","Hijyen"),
    ("Fiyat","Fiyat"),
)

personel_choice=(
    ("Doktor" , "Doktor"),
    ("Hemşire", "Hemşire"),
    ("Eczacı", "Eczacı"),
    ("Diş Hekimi", "Diş Hekimi"),
    ("Fizyoterapist","Fizyoterapist"),
    ("Ebe","Ebe"),
    ("Anestezi Teknikeri","Anestezi Teknikeri"),
    ("Laboratuvar Teknikeri","Laboratuvar Teknikeri"),
    ("Odyometri Teknikeri","Odyometri Teknikeri"),
    ("Ameliyathane Teknikeri","Ameliyathane Teknikeri"),
    ("Radyoloji Teknikeri","Radyoloji Teknikeri"),
    ("Sekreter","Sekreter"),
    ("Temizlik Personeli","Temizlik Personeli"),
    ("Güvenlik", "Güvenlik"),
    ("Hasta Bakıcı","Hasta Bakıcı"),
    ("Diğer","Diğer"),
)

priority_choice=(
    ("Normal","Normal"),
    ("Orta","Orta"),
    ("Yüksek","Yüksek"),
)

f_status_choice = (
    ("Açık","Açık"),
    ("İşlemde","İşlemde"),
    ("Çözüldü","Çözüldü"),
)

class Country(models.Model):
    name = models.CharField(max_length=27,verbose_name="name",default="Türkiye")
    def __str__(self):
        return self.name

class City(models.Model):
    IdCountry = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="country")
    name = models.CharField(max_length=27,verbose_name="city")
    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100,verbose_name="company_name")
    status = models.CharField(max_length=5,verbose_name="company_status",default="Pasif",choices=status_choices)
    idcountry = models.ForeignKey(Country,on_delete=models.CASCADE,verbose_name="idcountry")
    idcity = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="idcity")
    address = models.TextField(max_length=150,verbose_name="adress")
    def __str__(self):
        return self.name

class Department(models.Model):
    idcompany= models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="dprt_company")
    name = models.CharField(max_length=50,verbose_name="Departman Adı")
    status = models.CharField(max_length=6,verbose_name="Durum",choices=status_choices)
    def __str__(self):
        return self.name

class FeedbackType(models.Model):
    idcompany= models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="f_type_company")
    name = models.CharField(max_length=8,verbose_name="Talep-Şikayet Tipi")
    status = models.CharField(max_length=6,verbose_name="Durum",choices=status_choices)
    def __str__(self):
        return self.name

class FeedbackReason(models.Model):
    idcompany= models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="f_reason_company")
    name = models.CharField(max_length=35,verbose_name="Talep-Şikayet Nedeni Adı")
    status = models.CharField(max_length=6,verbose_name="Durum",choices=status_choices)
    def __str__(self):
        return self.name

class FeedbackSource(models.Model):
    idcompany= models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="f_source_company")
    name = models.CharField(max_length=35,verbose_name="Talep-Şikayet Genel Neden Adı")
    status = models.CharField(max_length=6,verbose_name="Durum",choices=status_choices)
    def __str__(self):
        return self.name

class FeedbackPersonel(models.Model):
    idcompany= models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="Hastane")
    name = models.CharField(max_length=35,verbose_name="Personel Adı")
    def __str__(self):
        return self.name

class FeedbackPriorityLevel(models.Model):
    idcompany= models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="f_priority_company")
    name = models.CharField(max_length=35,verbose_name="f_priority_name",choices=priority_choice)
    def __str__(self):
        return self.name


class FeedbackStatus(models.Model):
    IdCompany = models.ForeignKey(Company,verbose_name="status_ıdcompany",on_delete=models.CASCADE)
    name = models.CharField(max_length=7,verbose_name="Durum Adı",choices=f_status_choice)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    IdCompany = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="Hastane")
    Name = models.CharField(max_length=30,verbose_name="Ad",null=True,blank=True)
    Surname = models.CharField(max_length=30,verbose_name="Soyad",null=True,blank=True)
    Email = models.EmailField(max_length=40,verbose_name="Email")
    PhoneNumber = PhoneNumberField(default="",verbose_name="Telefon Numarası")
    Content = models.TextField(verbose_name="Talep-Şikayet İçeriği")
    Photo = models.FileField(blank=True,null=True,verbose_name="Resim")
    IdDepartment = models.ForeignKey(Department,on_delete=models.CASCADE,verbose_name="Talep-Şikayet Departmanı")
    IdFeedbackType = models.ForeignKey(FeedbackType,on_delete=models.CASCADE,verbose_name="Talep-Şikayet Tipi")
    IdFeedbackSource = models.ManyToManyField(FeedbackSource,verbose_name="Talep-Şikayet Nedeni (Çoklu Seçim Yapılabilir) ")
    IdFeedbackReason = models.ManyToManyField(FeedbackReason,verbose_name="Talep-Şikayet Nedeni (Detay) (Çoklu Seçim Yapılabilir) ")
    IdFeedbackPersonel =models.ManyToManyField(FeedbackPersonel,verbose_name="Talep-Şikayet Personeli (Çoklu Seçim Yapılabilir) ")
    FeedbackOpenDate = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    IdFeedbackPriorityLevel = models.ForeignKey(FeedbackPriorityLevel,null=True,on_delete=models.CASCADE,verbose_name="Talep-Şikayet Öncelik Seviyesi")
    IdFeedbackStatus = models.ForeignKey(FeedbackStatus,default=1,verbose_name="Talep-Şikayet Durumu",on_delete=models.CASCADE)
    FeedbackClosedDate= models.DateTimeField(auto_now=True,verbose_name="Talep-Şikayet Son İşlem Saati")
    LastSolveDate = models.DateTimeField(null=True,verbose_name="Talep ve Şikayetin Yanıtı İçin Gerekli Zaman(Ör: ..-..-.... 17:40)")
    DurationTime = models.CharField(max_length=100,verbose_name="Geçen Zaman",null=True)
    
    def __str__(self):
        return self.Content

    class Meta:
        ordering = ["IdFeedbackStatus__id","-IdFeedbackPriorityLevel__id"]

    
class FeedbackStatusHistory(models.Model):
    history_feedback = models.ForeignKey(Feedback,verbose_name="history_feedback",on_delete=models.CASCADE)
    history_status = models.ForeignKey(FeedbackStatus,verbose_name="Talep-Şikayet Durumu",on_delete=models.CASCADE)
    history_department = models.ForeignKey(Department,verbose_name="Talep-Şikayet Departmanı",on_delete=models.CASCADE)
    history_user = models.ForeignKey(User,verbose_name="Talep-Şikayet Kontrolü Yapan Kişi",on_delete=models.CASCADE)
    history_date = models.DateTimeField(auto_now_add=True,verbose_name="Geri Bildirim Tarihi")
    history_note = models.TextField(null=True,verbose_name="Geri Bildirim Notu")
    history_file = models.FileField(blank=True,null=True,verbose_name="Geri Bildirim Dosyası")

    def __str__(self):
        return self.history_note

