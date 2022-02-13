from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('login/', views.loginPage, name= 'login'),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name='register'),
    path('home/', views.home, name= 'home'),
    path('create-wallet/', views.createWallet, name= 'create-wallet'),
    path('wallet/', views.wallet, name= 'wallet'),
    path('Buy_data/', views.BuyData, name='Buy-data'),
    path('Bundle/<str:pk>/', views.Bundle_detail, name='Bundle'),
    path('callback/', views.payment_response, name='payment_response')
    
]
