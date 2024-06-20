from django.urls import path
from . import views


app_name = 'sitemembers'

urlpatterns = [
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('registeruser/', views.registeruser, name='registeruser'),
]
