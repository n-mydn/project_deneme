from django.urls import path
from . import views

app_name="feedback"

urlpatterns = [
    path('feedback/',views.feedback,name="feedback"),

   
    path('admin_all_department',views.admin_all_department,name="admin_all_department"),
    path('department_delete/<int:id>',views.department_delete,name="department_delete"),
    path('department_update/<int:id>',views.department_update,name="department_update"),
    path('admin_all_feedback',views.admin_all_feedback,name="admin_all_feedback"),
    path('admin_feedback',views.admin_feedback,name="admin_feedback"),
    path('admin_feedback_detail/<int:id>',views.admin_feedback_detail,name="admin_feedback_detail"),
    path('admin_feedback_islemde',views.admin_feedback_islemde,name="admin_feedback_islemde"),
    path('admin_feedback_cozuldu',views.admin_feedback_cozuldu,name="admin_feedback_cozuldu"),
    path('aktif_pasif_update/<int:id>',views.aktif_pasif_update,name="aktif_pasif_update"),
    path('feedback_type',views.feedback_type,name="feedback_type"),
    path('feedback_type_update/<int:id>',views.feedback_type_update,name="feedback_type_update"),
    path('feedback_type_delete/<int:id>',views.feedback_type_delete,name="feedback_type_delete"),
    path('admin_personel',views.admin_personel,name="admin_personel"),
    path('admin_personel_update/<int:id>',views.admin_personel_update,name="admin_personel_update"),
    path('admin_personel_delete/<int:id>',views.admin_personel_delete,name="admin_personel_delete"),
    path('feedback_reason',views.feedback_reason,name="feedback_reason"),
    path('feedback_source',views.feedback_source,name="feedback_source"),
    path('feedback_reason_delete/<int:id>',views.feedback_reason_delete,name="feedback_reason_delete"),
    path('feedback_source_delete/<int:id>',views.feedback_source_delete,name="feedback_source_delete"),
    path('feedback_reason_update/<int:id>',views.feedback_reason_update,name="feedback_reason_update"),
    path('feedback_source_update/<int:id>',views.feedback_source_update,name="feedback_source_update"),
    path('admin_register',views.admin_register,name="admin_register"),
    path('admin_register_update/<int:id>',views.admin_register_update,name="admin_register_update"),
    path('admin_register_delete/<int:id>',views.admin_register_delete,name="admin_register_delete"),
    path('admin_register_personel',views.admin_register_personel,name="admin_register_personel"),
    path('admin_register_personel_update/<int:id>',views.admin_register_personel_update,name="admin_register_personel_update"),
    path('admin_register_personel_delete/<int:id>',views.admin_register_personel_delete,name="admin_register_personel_delete"),


    path('d_admin_index',views.d_admin_index,name="d_admin_index"),
    path('d_admin_feedback_detail/<int:id>',views.d_admin_feedback_detail,name="d_admin_feedback_detail"),
    path('d_admin_cozuldu',views.d_admin_cozuldu,name="d_admin_cozuldu"),
    path('files_read/<int:id>',views.files_read,name="files_read"),
    path('d_admin_update',views.d_admin_update,name="d_admin_update"),

]

"""
  path('feedback_status_create/<int:id>',views.feedback_status_create,name="feedback_status_create"),
  path('feedback_detail/<int:id>',views.feedback_detail,name="feedback_detail"),
  path('feedbackdepartment_update/<int:id>',views.feedbackdepartment_update,name="feedbackdepartment_update"),

   path('feedback_status_update/<int:id>',views.feedback_status_update,name="feedback_status_update"), ---> department_admin/feedback_status sil

  path('admin_index',views.admin_index,name="admin_index"),

  path('feedback_admin_update/<int:id>',views.feedback_admin_update,name="feedback_admin_update"), ---->admin/feedback_admin_update , feedback_admin_update.html

  admin_department.html sill!!!
"""