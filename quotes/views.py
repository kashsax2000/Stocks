from .models import Stock
from django.http import HttpResponse
from .forms import StockForm
from django.contrib.auth import login , authenticate , logout
from django.shortcuts import render,redirect 
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib import auth
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def home(request):
	import requests
	import json


	if request.method == 'POST':
		ticker = request.POST['ticker']

		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_8ae8318490294dd09e9397ef7c4a8a1f")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request,'home.html',{'api':api})
	else:
		return render(request,'home.html',{'ticker':"Enter a ticker above..."})
	# API token: pk_8ae8318490294dd09e9397ef7c4a8a1f

def about(request):
	return render(request,'about.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')
            
    context = {'form':form} 
    return render(request, "register.html",context)


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:

            messages.info(request,'Username or password is incorrect')
    context = {} 
    return render(request, "login.html",context)

def logoutuser(request): 
    logout(request)
    return redirect('login')

@login_required
def converter(request):
	return render(request,'converter.html')

@login_required(redirect_field_name='next', login_url=userlogin)
def addStock(request):
	import requests
	import json


	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request,("Stocks has been Added!"))
			return redirect('addStock')

	else:
		ticker = Stock.objects.all()
		output = []

		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_fd84c9a9dfd049d9a6c431879c1b9ae9")

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request,'addStock.html',{'ticker':ticker, 'output': output})

@login_required(redirect_field_name='next', login_url=userlogin)
def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,("Stock has been deleted!"))
	return redirect(addStock)

@login_required(redirect_field_name='next', login_url=userlogin)
def visualize(request):
	return render(request,'visualize.html')

@login_required(redirect_field_name='next', login_url=userlogin)
def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html',{'ticker':ticker})
