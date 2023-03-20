from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
]

"""
    path("d_login",views.d_login,name="d_login"),
    path("a_login",views.a_login,name="a_login"),
"""