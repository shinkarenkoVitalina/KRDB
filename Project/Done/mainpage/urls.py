from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('ver/<str:token>', views.ConfirmReg),
    path('confirmuser/', views.DoneReg, name = 'confirmuser'),
    path('registration/', views.registration),
    path('autorization/', views.autorization),
    path('reguser', views.RegUser, name = "reguser"),
    path('authuser', views.AuthUser, name = "authuser")
]

