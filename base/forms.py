from dataclasses import fields
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import *

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        
class WalletForm(ModelForm):
    class Meta:
        model = Wallet
        fields = '__all__'
        exclude = ['user', 'Data_balance']

class PaymentForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField()
    phone=forms.CharField(max_length=15)
    amount = forms.FloatField()    
    
   