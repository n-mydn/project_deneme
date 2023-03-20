from django.shortcuts import render,redirect,get_object_or_404
from .models import Feedback,Department,FeedbackStatusHistory,FeedbackType,FeedbackReason,FeedbackSource,FeedbackPersonel,Company
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .forms import FeedbackForm,AdminFeedbackForm,DepartmentForm,StatusHistoryForm,StatusForm,FeedbackPersonelForm,FeedbackReasonForm,FeedbackTypeForm,FeedbackSourceForm
from django.contrib import messages
from django.utils.timezone import now
from user.models import UserAddProfile
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from project import settings
from user.forms import RegisterAddForm,AdminUserAddForm,AdminUserForm,RegisterFrom
from user.models import User,UserAddProfile
from django.contrib.auth import login as auth_login
from feedback.models import type_choice
import random
import string
# Create your views here.

def zaman(feedback):
        liste = list()
        time = now() - feedback.FeedbackOpenDate
        for t in str(time):
            liste.append(t)
        if liste[2] == "d":
            time = liste[0] + " gün"
        elif liste[0]=="0" and liste[1]==":":
            time = liste[2]+liste[3]+" dakika"
        elif liste[3]=="d":
            time = liste[0]+liste[1]+" gün"
        elif liste[1]==":" and int(liste[2]) == True :
            time = liste[0]+liste[1]+ " saat"
        elif liste[2] == ":" :
            time = liste[0]+liste[1]+ " saat"
        elif liste[1] == ":":
            time =liste[0]+ " saat"
        elif liste[2]=="m":
            time = liste[0] +" ay"
        elif liste[3]=="m":
            time = liste[0]+liste[1]+" ay"
        feedback.DurationTime = time
        feedback.save()

def random_string():
    liste= list()
    l_chars = string.ascii_lowercase
    u_chars =string.ascii_uppercase
    d_chars = string.digits
    kullanıcı = l_chars+u_chars+d_chars
    sifre = d_chars
    data = random.sample(kullanıcı,8)
    data_sifre = random.sample(sifre,6)
    kullanıcı_adı = "".join(data)
    kullanıcı_sifre = "".join(data_sifre)
    liste.append(kullanıcı_adı)
    liste.append(kullanıcı_sifre)
    return liste

def mail_gonderme(email):
    deger = random_string()
    subject = "Talep-Şikayet Giriş Kodu"
    message = "Talep-Şikayet durumunuzu kontrol etmek için 'Kullanıcı Adı: {} - Şifre:{}' ile giriş yapabilirsiniz".format(deger[0],deger[1])
    send_mail( subject, message, '', email)


# --------------- Departman Admini ---------------
@login_required(login_url="user:login")
def d_admin_index(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    department = d_user.user_department
    feedbacks_list = Feedback.objects.filter(IdDepartment=department.id,IdFeedbackStatus=2)

    paginator = Paginator(feedbacks_list, 1)  # Show 5 contacts per page
    page = request.GET.get('sayfa')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedbacks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedbacks = paginator.page(paginator.num_pages)

    sayı = 0
    for feedback in feedbacks_list:
        zaman(feedback)
        if FeedbackStatusHistory.objects.filter(history_feedback_id=feedback.id).first()==None and feedback.FeedbackClosedDate > feedback.LastSolveDate:
            sayı +=1
           

    keyword = request.GET.get("keyword") 
    if keyword:
        feedbacks = Feedback.objects.filter(
            Q(IdDepartment=department.id),
            Q(IdFeedbackStatus = 2),
            Q(IdFeedbackPriorityLevel__name__icontains=keyword)
        ).distinct()
    context = {
        "department":department,
        "feedbacks":feedbacks,
        "sayı":sayı,
    } 
    return render(request,"department_admin/index.html",context)

@login_required(login_url="user:login")
def d_admin_update(request):
    k_user = request.user
    currentpassword = request.user.password 
    user = User.objects.filter(id=k_user.id).first()
    bilgi2 = UserAddProfile.objects.filter(user__id=k_user.id).first()
    form2 = RegisterAddForm(request.POST or None,instance=bilgi2)
    context={
        "user":user,
        "form2":form2
    }
    if form2.is_valid():
        last_password=request.POST.get("last_password")
        password=request.POST.get("password")
        confirm = request.POST.get("confirm")
        first_name = request.POST.get("first_name")
        last_name =request.POST.get("last_name")
        email = request.POST.get("email")

        check = check_password(last_password,currentpassword)
        if last_password == "":
            messages.info(request,"Bilgi Güncellemek İçin Kullanılan Şifre Kısmını Doldurunuz!")
            return render(request,"department_admin/d_admin_update.html",context)

        if check == False:
            messages.info(request,"Kullanıcı Şifrenizi Yanlış Girdiniz!")
            messages.info(request,"Güncelleme Tamamlanamadı!")
            return render(request,"department_admin/d_admin_update.html",context)
        
        try:
            if password != "" and last_password != "" and confirm != "" :
                if password != confirm:
                    messages.info(request,"Yeni Parola-Yeni Parola(Tekrar) Aynı Değil!")
                    messages.info(request,"Güncelleme Tamamlanamadı!")
                    return render(request,"department_admin/d_admin_update.html",context)
                user.set_password(password) 
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.save()
            b_user = form2.save(commit=False)
            b_user.user_id = user.id
            b_user.save()
            auth_login(request,user)
            messages.success(request,"Bilgileriniz Başarıyla Güncellendi.")
            return redirect("feedback:d_admin_update")
        except:
            messages.info(request,"Bilgileriniz Güncellenemedi!")
            return render(request,"department_admin/d_admin_update.html",context)
        
    return render(request,"department_admin/d_admin_update.html",context)

@login_required(login_url="user:login")
def d_admin_feedback_detail(request,id):
    feedback = Feedback.objects.filter(id=id).first()
    feedback_status = FeedbackStatusHistory.objects.filter(history_feedback=id).first()
    form = StatusHistoryForm(request.POST or None,request.FILES or None,instance=feedback_status)
    zaman(feedback) #olmazsa zaman altında olanı kopyala yapıştır!
    context = {
        "feedback":feedback, 
        "feedback_status":feedback_status,
        "form":form,
    }
    if form.is_valid():
        status = form.save(commit = False)
        status.history_feedback_id = id
        status.history_status_id = feedback.IdFeedbackStatus.id
        status.history_department_id = feedback.IdDepartment.id
        status.history_user = request.user
        status.save()
        messages.success(request,"Talep-Şikayet Geri Bildirimi Oluşturuldu.")
        return redirect("feedback:d_admin_feedback_detail",id=feedback.id)
    return render(request,"department_admin/feedback_detail.html",context)

@login_required(login_url="user:login")
def d_admin_cozuldu(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    department = d_user.user_department
    feedbacks_list = Feedback.objects.filter(IdCompany=company_id,IdFeedbackStatus__name="Çözüldü").order_by('-FeedbackOpenDate')

    feedbacks_sayı = Feedback.objects.filter(IdDepartment=department.id,IdFeedbackStatus=2)
    sayı = 0
    for feedback in feedbacks_sayı:
        zaman(feedback)
        if FeedbackStatusHistory.objects.filter(history_feedback_id=feedback.id).first()==None and feedback.FeedbackClosedDate > feedback.LastSolveDate:
            sayı +=1
    paginator = Paginator(feedbacks_list, 1)  # Show 5 contacts per page
    page = request.GET.get('sayfa')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedbacks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages.warning(request,"Geçerli olmayan sayfa numarası!")
        feedbacks = paginator.page(paginator.num_pages)
    context = {
        "department":department,
        "feedbacks":feedbacks,
        "sayı":sayı
    }
    return render(request,"department_admin/d_admin_cozuldu.html",context)

"""
@login_required(login_url="user:login")
def feedback_status_update(request,id):
    feedback = Feedback.objects.filter(id=id).first()
    feedback_status = FeedbackStatusHistory.objects.filter(history_feedback = id).first()
    form = StatusHistoryForm(request.POST or None,request.FILES or None,instance=feedback_status)
    context={
        "form":form,
        "feedback":feedback,
        "feedback_status":feedback_status,
    }
    if form.is_valid():
        status = form.save(commit = False)
        status.history_feedback_id = id
        status.history_status_id = feedback.IdFeedbackStatus.id
        status.history_department_id = feedback.IdDepartment.id
        status.history_user = request.user
        status.save()
        messages.success(request,"Talep-Şikayet Yanıtları Oluşturuldu.")
        return redirect("feedback:d_admin_index")

    return render(request,"department_admin/feedback_status.html",context)
"""

@login_required(login_url="user:login")
def files_read(request,id):
    feedback_status = FeedbackStatusHistory.objects.filter(id=id).first()
    with open(feedback_status.history_file.path,"r",encoding="utf-8") as file:
        f = file.read()
        return render(request,"files_read.html",{"f":f})

#-----------------------------------------------------------------------------
def index(request):
    return render(request,"index.html")

login_required(login_url="user:login")
def feedback(request):
    form = FeedbackForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        id = request.POST["IdDepartment"]
        email = request.POST["Email"]
        department = Department.objects.filter(id=id).first()
        if department.status == "Pasif" :
            messages.info(request,"{} Departmanı Şu An Aktif Değildir!".format(department.name))
            messages.info(request,"Departman Seçiminizi Tekrar Kontrol Ediniz!")
            return render(request,"feedback_create.html",{"form":form})
        form.save()
        messages.success(request,"Talep-Şikayet Başarıyla Oluşturuldu.")
        #mail_gonderme([email])
        #messages.success(request,"Mailinize Gelen Bilgilerle Giriş Yapabilirsiniz!")
        return redirect("index")
    return render(request,"feedback_create.html",{"form":form})

"""
@login_required(login_url="user:login")
def all_department(request):
    departments = Department.objects.all()
    context = {
        "departments":departments
    }
    return render(request,"all_department.html",context)


@login_required(login_url="user:login")
def department_detail(request,id):
    dprt = Department.objects.filter(id=id).first()
    feedbacks = Feedback.objects.filter(IdDepartment=id)
    context = {
        "dprt":dprt,
        "feedbacks":feedbacks,
    }
    return render(request,"department_detail.html",context)

@login_required(login_url="user:login")
def feedback_detail(request,id):
    feedback = Feedback.objects.filter(id=id).first()
    context={
        "feedback":feedback
    }
    return render(request,"feedback_detail.html",context)

@login_required(login_url="user:login")
def feedbackdepartment_update(request,id):
    pass
"""

# ----------------- ADMİN BÖLÜMÜ -----------------
"""
def admin_index(request):
    return render(request,"admin/all_department.html")
"""

@login_required(login_url="user:login")
def admin_all_department(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    hastane_id = d_user.user_company
    departments_list = Department.objects.filter(idcompany=hastane_id,status="Aktif").order_by("id")
    paginator = Paginator(departments_list, 7)
    page = request.GET.get('sayfa')
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)
    form = DepartmentForm(request.POST or None)
    context={
        "departments":departments,
        "form":form
    }
    if form.is_valid():
        dprt = form.save(commit=False)
        dprt.idcompany = hastane_id
        dprt.save()
        messages.success(request,"Departman Başarıyla Oluşturuldu.")
        return render(request,"admin/all_department.html",context)
    return render(request,"admin/all_department.html",context)


@login_required(login_url="user:login")
def department_update(request,id):
    department = Department.objects.get(id=id)
    form_update = DepartmentForm(request.POST or None,instance=department)
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    hastane_id = d_user.user_company
    departments_list = Department.objects.filter(idcompany=hastane_id).order_by("id")
    paginator = Paginator(departments_list, 7)
    page = request.GET.get('sayfa')
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)

    context={
        "form_update":form_update,
        "department":department,
        "departments":departments,
        "id":id,
    }
    if form_update.is_valid():
        dprt = form_update.save(commit=False)
        dprt.idcompany = department.idcompany
        dprt.save()
        messages.success(request,"Departman Bilgileri Güncellendi.")
        return render(request,"admin/all_department.html",context)
    
    return render(request,"admin/department_update.html",context)

@login_required(login_url="user:login")
def department_delete(request,id):
    department = Department.objects.get(id=id)
    department.delete()
    messages.success(request,"Departman Bilgileri Silindi")
    return redirect("feedback:admin_all_department")


@login_required(login_url="user:login")
def feedback_type(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    feedback_types = FeedbackType.objects.filter(idcompany=company_id)
    form = FeedbackTypeForm(request.POST or None)
    context={
        "feedback_types":feedback_types,
        "form":form
    }
    if form.is_valid():
        f_type = form.save(commit=False)
        f_type.idcompany = company_id
        f_type.save()
        messages.success(request,"Talep-Şikayet Tipi Oluşturuldu")
        return redirect("feedback:feedback_type")
    return render(request,"admin/feedback_type.html",context)


@login_required(login_url="user:login")
def feedback_type_update(request,id):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    feedback_types = FeedbackType.objects.filter(idcompany=company_id)
    feedback_type = FeedbackType.objects.get(id=id)
    form = FeedbackTypeForm(request.POST or None,instance=feedback_type)
    context={
        "feedback_types":feedback_types,
        "form":form,
        "id":id
    }
    if form.is_valid():
        if form.has_changed() == False:
            messages.info(request,"Talep-Şikayet Tipinde Değişiklik Olmadı!")
            return render(request,"admin/feedback_type_update.html",context)
        f_type = form.save(commit=False)
        f_type.idcompany = company_id
        f_type.save()
        messages.success(request,"Talep-Şikayet Tipi Güncellendi")
        return redirect("feedback:feedback_type")
    return render(request,"admin/feedback_type_update.html",context)


@login_required(login_url="user:login")
def feedback_type_delete(request,id):
    feedback_type = FeedbackType.objects.get(id=id)
    feedback_type.delete()
    messages.success(request,"Talep-Şikayet Tipi Silindi")
    return redirect("feedback:feedback_type")

@login_required(login_url="user:login")
def admin_all_feedback(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    feedbacks_list = Feedback.objects.filter(IdCompany=company_id)
    for feedback in feedbacks_list:
        zaman(feedback)

    sayı = 0
    for feedback in feedbacks_list:
        zaman(feedback)
        if feedback.LastSolveDate != None:
            if feedback.FeedbackClosedDate > feedback.LastSolveDate:
                sayı +=1
    paginator = Paginator(feedbacks_list,1) #10 yap 
    page = request.GET.get('sayfa')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)
    
    keyword = request.GET.get("keyword") 
    if keyword:
        feedbacks = Feedback.objects.filter(
            Q(IdDepartment__name__icontains=keyword),
            Q(IdCompany=company_id),
        ).distinct()
    context={
        "feedbacks":feedbacks,
        "sayı":sayı
    }
    return render(request,"admin/index.html",context)


@login_required(login_url="user:login")
def admin_feedback_detail(request,id):
    feedback = Feedback.objects.get(id=id)
    zaman(feedback)
    form = AdminFeedbackForm(request.POST or None,instance=feedback)
    feedback_status = FeedbackStatusHistory.objects.filter(history_feedback=id).first()
    status_form = StatusForm(request.POST or None,instance=feedback)
    context = {
        "feedback":feedback,
        "form":form,
        "feedback_status":feedback_status,
        "status_form":status_form,
    }
    
    if form.is_valid():
        feedback = form.save(commit=False)
        if form.has_changed() == False:
            messages.info(request,"Talep-Şikayet Bilgilerinde Değişiklik Olmadı!")
            return redirect("feedback:admin_feedback_detail",id=feedback.id)
        if feedback.IdFeedbackStatus.id != 2:
            messages.info(request,"Talep-Şikayet Durumu 'İşlemde' Olmalıdır!")
            return redirect("feedback:admin_feedback_detail",id=feedback.id)
        if feedback.LastSolveDate < feedback.FeedbackClosedDate :
            messages.info(request,"Talep-Şikayet İçin Gerekli Zaman Geçmiş Zaman Olamaz!")
            return redirect("feedback:admin_feedback_detail",id=feedback.id)
        feedback.save()
        messages.success(request,"Talep-Şikayet Bilgileri Güncellendi.")
        return redirect("feedback:admin_all_feedback")
    
    if status_form.is_valid():
        status = status_form.save(commit=False)
        if status.IdFeedbackStatus.id != 3:
            messages.info(request,"Talep-Şikayet Durumu 'ÇÖZÜLDÜ' Olmalıdır!")
            return render(request,"admin/feedback_detail.html",context)
        status.save()
        zaman(feedback)
        feedback_status.history_status_id = 3
        feedback_status.save()
        messages.success(request,"Talep-Şikayet Durumu Güncellendi.")
        return redirect("feedback:admin_all_feedback")
    
    return render(request,"admin/feedback_detail.html",context)



"""
@login_required(login_url="user:login")
def feedback_admin_update(request,id):
    feedback = Feedback.objects.get(id=id)
    form = AdminFeedbackForm(request.POST or None,instance=feedback)
    feedback_status = FeedbackStatusHistory.objects.filter(history_feedback=id).first()
    status_form = StatusForm(request.POST or None,instance=feedback)
    context = {
        "feedback":feedback,
        "form":form,
        "feedback_status":feedback_status,
        "status_form":status_form,
    }
    if form.is_valid():
        feedback = form.save(commit=False)
        if feedback.IdFeedbackStatus.id != 2:
            messages.info(request,"Talep-Şikayet Durumu 'İşlemde' Olmalıdır!")
            return render(request,"admin/feedback_admin_update.html",context)
        if feedback.LastSolveDate < feedback.FeedbackClosedDate :
            messages.info(request,"Talep-Şikayet İçin Gerekli Zaman Geçmiş Zaman Olamaz!")
            return render(request,"admin/feedback_admin_update.html",context)
            
        zaman(feedback) #olmazsa zaman altında olanı kopyala yapıştır!
        messages.success(request,"Talep-Şikayet Bilgileri Güncellendi.")
        return redirect("feedback:admin_department",id=feedback.IdDepartment.id)
    
    if status_form.is_valid():
        status = status_form.save(commit=False)
        if status.IdFeedbackStatus.id != 3:
            messages.info(request,"Talep-Şikayet Durumu 'ÇÖZÜLDÜ' Olmalıdır!")
            return render(request,"admin/feedback_admin_update.html",context)
        status.save()
        zaman(feedback) #olmazsa zaman altında olanı kopyala yapıştır!
        feedback_status.history_status_id = 3
        feedback_status.save()
        messages.success(request,"Talep-Şikayet Durumu Güncellendi.")
        return redirect("feedback:admin_department",id=feedback.IdDepartment.id)

    return render(request,"admin/feedback_admin_update.html",context)
"""

@login_required(login_url="user:login")
def admin_feedback(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    feedbacks_list = Feedback.objects.filter(IdCompany=company_id,IdFeedbackStatus__name="Açık")
    for feedback in feedbacks_list:
        zaman(feedback)
 
    paginator = Paginator(feedbacks_list,1) #10 yap 
    page = request.GET.get('sayfa')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)
    context = {
        "feedbacks":feedbacks
    }
    return render(request,"admin/admin_feedback.html",context)


@login_required(login_url="user:login")
def admin_feedback_islemde(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    feedbacks_list = Feedback.objects.filter(IdCompany=company_id,IdFeedbackStatus__name="İşlemde")

    paginator = Paginator(feedbacks_list, 1)  # Show 5 contacts per page
    page = request.GET.get('sayfa')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedbacks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages.warning(request,"Geçerli olmayan sayfa numarası!")
        feedbacks = paginator.page(paginator.num_pages)

    liste = list()
    for feedback in feedbacks_list:
        zaman(feedback)
        feedback_status = FeedbackStatusHistory.objects.filter(
            Q(history_feedback_id=feedback.pk),
            Q(history_department_id=feedback.IdDepartment),
            Q(history_status_id=2)
        ).distinct()
        if feedback_status.first() != None:
            liste.append(feedback_status)
    context = {
        "feedbacks":feedbacks,
        "liste":liste,
        "bildirim":len(liste),
    }
    return render(request,"admin/admin_feedback_islemde.html",context)

@login_required(login_url="user:login")
def admin_feedback_cozuldu(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    feedbacks_list = Feedback.objects.filter(IdCompany=company_id,IdFeedbackStatus__name="Çözüldü")
    paginator = Paginator(feedbacks_list, 1)  # Show 5 contacts per page
    page = request.GET.get('sayfa')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedbacks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages.warning(request,"Geçerli olmayan sayfa numarası!")
        feedbacks = paginator.page(paginator.num_pages)
    context = {
        "feedbacks":feedbacks
    }
    return render(request,"admin/admin_feedback_cozuldu.html",context)


@login_required(login_url="user:login")
def admin_personel(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    personel_list = FeedbackPersonel.objects.filter(idcompany=company_id)
    form = FeedbackPersonelForm(request.POST or None)
    paginator = Paginator(personel_list, 7)
    page = request.GET.get('sayfa')
    try:
        personel_all = paginator.page(page)
    except PageNotAnInteger:
        personel_all = paginator.page(1)
    except EmptyPage:
        personel_all = paginator.page(paginator.num_pages)
    context={
        "personel_all":personel_all,
        "form":form
    }
    if form.is_valid():
        f_type = form.save(commit=False)
        f_type.idcompany = company_id
        f_type.save()
        messages.success(request,"Personel Oluşturuldu.")
        return render(request,"admin/admin_personel.html",context)
    return render(request,"admin/admin_personel.html",context)


@login_required(login_url="user:login")
def admin_personel_update(request,id):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    personel_list = FeedbackPersonel.objects.filter(idcompany=company_id)
    personel = FeedbackPersonel.objects.get(id=id)
    form = FeedbackPersonelForm(request.POST or None,instance=personel)
    paginator = Paginator(personel_list, 7)
    page = request.GET.get('sayfa')
    try:
        personel_all = paginator.page(page)
    except PageNotAnInteger:
        personel_all = paginator.page(1)
    except EmptyPage:
        personel_all = paginator.page(paginator.num_pages)
    context={
        "personel_all":personel_all,
        "form":form,
        "id":id,
    }
    if form.is_valid():
        per = form.save(commit=False)
        per.idcompany = company_id
        per.save()
        messages.success(request,"Personel Bilgileri Güncellendi .")
        return redirect("feedback:admin_personel")
    
    return render(request,"admin/admin_personel_update.html",context)


@login_required(login_url="user:login")
def admin_personel_delete(request,id):
    personel = FeedbackPersonel.objects.get(id=id)
    personel.delete()
    messages.success(request,"Personel Bilgileri Silindi.")
    return redirect("feedback:admin_personel")


@login_required(login_url="user:login")
def feedback_source(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    source_all = FeedbackSource.objects.filter(idcompany=company_id)
    form_source = FeedbackSourceForm(request.POST or None)
    context={
        "source_all":source_all,
        "form_source":form_source,
    }

    if form_source.is_valid():
        f_source = form_source.save(commit=False)
        f_source.idcompany = company_id
        f_source.save()
        messages.success(request,"Talep-Şikayet Genel Nedeni Oluşturuldu.")
        return render(request,"admin/feedback_source.html",context)
    return render(request,"admin/feedback_source.html",context)


@login_required(login_url="user:login")
def feedback_reason(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    reason_all = FeedbackReason.objects.filter(idcompany=company_id)
    form_reason = FeedbackReasonForm(request.POST or None)
    context={
        "reason_all":reason_all,
        "form_reason":form_reason,
    }
    if form_reason.is_valid():
        f_reason = form_reason.save(commit=False)
        f_reason.idcompany = company_id
        f_reason.save()
        messages.success(request,"Talep-Şikayet Nedeni Oluşturuldu.")
        return render(request,"admin/feedback_reason.html",context)
    
    return render(request,"admin/feedback_reason.html",context)


@login_required(login_url="user:login")
def feedback_reason_update(request,id):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    reason_all = FeedbackReason.objects.filter(idcompany=company_id)
    reason = FeedbackReason.objects.get(id=id)
    form_reason = FeedbackReasonForm(request.POST or None,instance=reason)
    context={
        "reason_all":reason_all,
        "form_reason":form_reason,
        "id":id,
    }
    if form_reason.is_valid():
        if form_reason.has_changed() == False:
            messages.info(request,"Talep-Şikayet Nedeninde Bir Değişiklik Olmadı!")
            return render(request,"admin/feedback_reason_update.html",context)            
        f_reason = form_reason.save(commit=False)
        f_reason.idcompany = company_id
        f_reason.save()
        messages.success(request,"Talep-Şikayet Nedeni Güncellendi.")
        return render(request,"admin/feedback_reason_update.html",context)
    return render(request,"admin/feedback_reason_update.html",context)


@login_required(login_url="user:login")
def feedback_source_update(request,id):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company
    source_all = FeedbackSource.objects.filter(idcompany=company_id)
    source = FeedbackSource.objects.get(id=id)
    form_source = FeedbackSourceForm(request.POST or None,instance=source)
    context={
        "form_source":form_source,
        "source_all":source_all,
        "id":id
    }
    if form_source.is_valid():
        if form_source.has_changed() == False :
            messages.info(request,"Talep-Şikayet Genel Nedeninde Bir Değişiklik Olmadı!")
            return render(request,"admin/feedback_source_update.html",context)
        f_source = form_source.save(commit=False)
        f_source.idcompany = company_id
        f_source.save()
        messages.success(request,"Talep-Şikayet Genel Neden Güncellendi.")
        return render(request,"admin/feedback_source_update.html",context)
    return render(request,"admin/feedback_source_update.html",context)


@login_required(login_url="user:login")
def feedback_reason_delete(request,id):
    feedback_reason = FeedbackReason.objects.get(id=id)
    feedback_reason.delete()
    messages.success(request,"Talep-Şikayet Nedeni Silindi.")
    return redirect("feedback:feedback_reason")


@login_required(login_url="user:login")
def feedback_source_delete(request,id):
    feedback_source = FeedbackSource.objects.get(id=id)
    feedback_source.delete()
    messages.success(request,"Talep-Şikayet Genel Neden Silindi.")
    return redirect("feedback:feedback_source")


@login_required(login_url="user:login")
def aktif_pasif_update(request,id):
    department = Department.objects.filter(id=id).first()
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        department = form.save(commit = False)
        if form.status.has_changed() == False :
            messages.info(request,"Departmanın Durumu Değişmedi.")
            return render(request,"admin/aktif_pasif_update.html",{"form":form})
        department.save()
        messages.success(request,"Departmanın Durumu Güncellendi.")
        return redirect("feedback:admin_all_department")
        
    return render(request,"admin/aktif_pasif_update.html",{"form":form})


@login_required(login_url="user:login")
def admin_register(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company.id
    user_all = UserAddProfile.objects.filter(user_company=company_id)
    user_profile = User.objects.all()
    user_add = AdminUserAddForm(request.POST or None)
    context={
        "user_all":user_all,
        "user_add":user_add,
        "user_profile":user_profile,
    }
    if user_add.is_valid():
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        
        if password != confirm:
            messages.info(request,"Parola ve Parola Doğrula Aynı Değil!")
            return render(request,"admin/admin_register.html",context)

        new_user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username)
        new_user.set_password(password)
        new_user.save()

        if new_user:
            user_add_profile = user_add.save(commit=False)
            user_add_profile.user_id = new_user.id
            user_add_profile.user_status = "Aktif"
            user_add_profile.user_adress = ""
            user_add_profile.user_city= d_user.user_city
            user_add_profile.user_country = d_user.user_country
            user_add_profile.user_company = d_user.user_company
            user_add_profile.save()
            messages.success(request,"Admin Oluşturuldu!")
            return redirect("feedback:admin_register")

    return render(request,"admin/admin_register.html",context)


@login_required(login_url="user:login")
def admin_register_update(request,id):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company.id
    user_all = UserAddProfile.objects.filter(user_company=company_id)
    user = UserAddProfile.objects.get(id=id)
    user_profile = User.objects.all()
    update_user = User.objects.get(id=user.user_id)
    user_form = AdminUserAddForm(request.POST or None,instance=user)
    context={
        "user_all":user_all,
        "user_form":user_form,
        "update_user":update_user,
        "id":id,
        "user_profile":user_profile,
    }

    if user_form.is_valid():
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        
        update_user.username=username
        update_user.first_name=first_name
        update_user.last_name=last_name
        update_user.email=email
        update_user.save()

        user_form.save()
        messages.success(request,"Kullanıcı Güncellendi.")
        return redirect("feedback:admin_register")
    
    return render(request,"admin/admin_register_update.html",context)
        


@login_required(login_url="login:user")
def admin_register_delete(request,id):
    user_add = UserAddProfile.objects.get(id = id)
    user = User.objects.get(id=user_add.user_id)
    user.delete()
    messages.success(request,"Kullanıcı Silindi.")
    return redirect("feedback:admin_register")


@login_required(login_url="login:user")
def admin_register_personel(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company.id
    user_all = UserAddProfile.objects.filter(user_company=company_id)
    user_profile = User.objects.all()
    user_add = AdminUserAddForm(request.POST or None)
    context={
        "user_all":user_all,
        "user_add":user_add,
        "user_profile":user_profile,
    }
    if user_add.is_valid():
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        new_user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=first_name+last_name)
        new_user.save()

        if new_user:
            user_add_profile = user_add.save(commit=False)
            user_add_profile.user_id = new_user.id
            user_add_profile.user_status = "Aktif"
            user_add_profile.user_adress = ""
            user_add_profile.user_city= d_user.user_city
            user_add_profile.user_country = d_user.user_country
            user_add_profile.user_company = d_user.user_company
            user_add_profile.save()
            messages.success(request,"Admin Oluşturuldu!")
            return redirect("feedback:admin_register_personel")

    return render(request,"admin/admin_register_personel.html",context)


@login_required(login_url="login:user")
def admin_register_personel_update(request,id):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company.id
    user_all = UserAddProfile.objects.filter(user_company=company_id)
    user = UserAddProfile.objects.get(id=id)
    user_profile = User.objects.all()
    update_user = User.objects.get(id=user.user_id)
    user_form = AdminUserAddForm(request.POST or None,instance=user)
    context={
        "user_all":user_all,
        "user_form":user_form,
        "update_user":update_user,
        "id":id,
        "user_profile":user_profile,
    }

    if user_form.is_valid():
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        
        update_user.first_name=first_name
        update_user.last_name=last_name
        update_user.email=email
        update_user.save()

        user_form.save()
        messages.success(request,"Kullanıcı Güncellendi.")
        return redirect("feedback:admin_register_personel")
    
    return render(request,"admin/admin_register_personel_update.html",context)

@login_required(login_url="login:user")
def admin_register_personel_delete(request,id):
    user_add = UserAddProfile.objects.get(id = id)
    user = User.objects.get(id=user_add.user_id)
    user.delete()
    messages.success(request,"Kullanıcı Silindi.")
    return redirect("feedback:admin_register_personel")





"""
@login_required(login_url="user:login")
def admin_register(request):
    k_user = request.user
    d_user = UserAddProfile.objects.filter(user=k_user).first()
    company_id = d_user.user_company.id
    user_all = UserAddProfile.objects.filter(user_company=company_id)
    user_instanse= UserAddProfile.objects.filter(user_company=company_id).first()
    form_register = RegisterFrom(request.POST or None)
    form_add = AdminUserAddForm( request.POST or None,user_instanse)
    context={
        "user_all":user_all,
        "form_add":form_add,
        "form_register":form_register,
    }
  
    if form_register.is_valid():
        password = form_register.cleaned_data.get("password")
        confirm = form_register.cleaned_data.get("confirm")
        first_name = form_register.cleaned_data.get("first_name")
        last_name = form_register.cleaned_data.get("last_name")
        email = form_register.cleaned_data.get("email")
        username = form_register.cleaned_data.get("username")         

        if password != confirm:
            messages.info(request,"Parola-Parola(Tekrar) Birbiriyle Eşleşmiyor!")
            return render(request,"admin/admin_register.html",context)
            
        newUser = User(first_name=first_name,last_name=last_name,email=email,username=username)
        newUser.set_password(password)
        new_user = newUser.save()
        
        if newUser:
            if form_add.is_valid():
                user_add = form_add.save(commit=False)
                user_add.user = newUser.id
                user_add.user_company = company_id
                user_add.user_status = "Aktif"
                user_add.user_contry = user_instanse.user_country
                user_add.user_city = user_instanse.user_city
                user_add.save()

                messages.success(request,"Admin Oluşturuldu!")
                return redirect("feedback:admin_register")
        else:
            messages.info(request,"Admin Oluşturulamadı!")
            return redirect("feedback:admin_register")

    
    return render(request,"admin/admin_register.html",context)
"""