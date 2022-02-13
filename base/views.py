from asyncio.windows_events import NULL
from gettext import translation
from urllib import response
from django.forms import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .models import *
from .forms import *
import requests
import math
import random



# Create your views here.

def index(request):
    return render(request, 'index.html')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
        else:
           messages.error(request, "Ooops!!! An error occured during registration") 
    return render(request, 'register.html', {'form': form})



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        
        # if not user.is_email_verified:
        #     messages.error(request, 
        #                    'Email is not verified, please check your mail for a verification link')

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password does not exit')
            
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def home(request):
    user = request.user
    Transactions = DataTransactions.objects.all()
    return render(request, 'home.html', {'Transaction': Transactions}
                  )


@login_required(login_url='login')
def createWallet(request):
    form = WalletForm()
    
    if request.method == 'POST':
        Wallet.objects.create(
            user = request.user,
            First_Name = request.POST.get('First_Name'),
            Last_Name = request.POST.get('Last_Name'),
            Phone_number = request.POST.get('Phone_number'),
            City = request.POST.get('City'),
            Gender = request.POST.get('Gender')
        )
        return redirect('home')
    return render(request, 'create_wallet.html', {'form': form})


@login_required(login_url='login')
def wallet(request):
    user = request.user
    
    try:
        wallet = user.wallet
    except:
        return redirect('create-wallet')
    
    return render(request, 'wallet.html', {'wallet': wallet})


@login_required(login_url='login')
def BuyData(request):
    user = request.user
    wallet = user.wallet

    Bundle = DataBundle.objects.all()
            
    return render(request, 'Buy_data.html', {'wallet': wallet, 'Bundle':Bundle})



@login_required(login_url='login')
def Bundle_detail(request, pk):
    
    global data
    data = DataBundle.objects.get(id=pk)
    
    form = PaymentForm()
    
    if request.method=='POST':
        form = PaymentForm(request.POST)
        
        global To_wallet
        To_wallet = request.POST.get('To_wallet')
        
        if form.is_valid():
             name=  form.cleaned_data['name']
             email = form.cleaned_data['email']
             amount = form.cleaned_data['amount']
             global phone
             phone = form.cleaned_data['phone']
             return redirect(str(process_payment(name,email,amount,phone)))
    
    return render(request, 'Bundle_detail.html', {'form': form, 'data': data})



def process_payment(name,email,amount,phone):
    auth_token = 'FLWSECK-5ed4e3336758240237ac05a2afa94a17-X'
    hed = {'Authorization': 'Bearer ' + auth_token}
    
    data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"NGN",
                "redirect_url":"http://127.0.0.1:8000/callback",
                "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Data Purchase",
                    "description":"Make payments to receive data value.",
                    "logo":"avatar.svg"
                }
                }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    return link

@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    transaction_id = request.GET.get('transaction_id', None)
    
    user = request.user
    wallet = user.wallet
    
    
    print(status)
    print(tx_ref)
    print(phone)
    
    if status == 'successful':
        if To_wallet == 'on':    
            DataTransactions.objects.create(
            user = request.user.username,
            Data_amount = data.Amount,
            TransactionID = transaction_id,
            Credit = True,
            To_wallet = True
                )
        
            wallet.Data_balance += data.Amount
            wallet.save()
            
        else:
            
            url = 'https://simhostng.com/api/ussd'
            params = {'apikey':'2e348467022bf696ff467ac0ccf64c2f27dd0e07f8dcec44c7ccaee026140ff8', 'server':'ERMTNFVCH', 'sim': '1', 'number': '*556#', 'ref': ''+str(math.floor(1000000 + random.random()*9000000))}
                    
            response = requests.post(url, params)
            
            res = response.json()  
            # print(res['data'][0]['id'])
            
            transaction_id = request.GET.get('transaction_id', None)
            print(transaction_id)
            
            DataTransactions.objects.create(
            user = request.user.username,
            Data_amount = data.Amount,
            TransactionID = transaction_id,
            Credit = True,
            To_wallet = False
                )
    
    return render(request, 'Payment_response.html', {'data': data})

