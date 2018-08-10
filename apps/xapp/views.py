from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def indexlogin(request):
    return render(request, 'xapp/login.html')


def register(request):
    return render(request, 'xapp/register.html')


def createuser(request):
    results = User.objects.regValidator(request.POST)
    print(results)
    if results[0]:
        request.session['id'] = results[1].id
        request.session['name'] = results[1].name
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
            return redirect('/register')


def loginprocess(request):
    results = User.objects.loginValidator(request.POST)
    if results[0]:
        request.session['id'] = results[1].id
        request.session['name'] = results[1].name
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


def dashboard(request, user_id=None):
    if 'id' not in request.session:
        return redirect('/')
    
    mywishlist = User.objects.get(id=request.session['id']).wishitems.all()
    productslist = Product.objects.exclude(wisher = request.session['id'])

    context = {
        'mywishlist' : mywishlist,
        'productslist' : productslist
    }
   
    return render(request, 'xapp/dashboard.html', context)


def add(request, user_id=None):
    return render(request, 'xapp/addproduct.html')



def addproduct(request, user_id=None):
    results = Product.objects.productValidator(request.POST, request.session['id'])
    if results[0]:
        return redirect('/dashboard/{}'.format(request.session['id']))
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='adderror')
            return redirect('/add/{}'.format(request.session['id']))



def showproduct(request, x):
    product = Product.objects.get(id=x)
    other_users = product.wisher.all()
    context = {
        'product' : product,
        'other_users' : other_users
    }
    return render(request, 'xapp/showproduct.html', context)


def addtowish(request, x):
    user = User.objects.get(id=request.session['id'])
    product = Product.objects.get(id=x)

    user.wishitems.add(product)
    
    return redirect('/dashboard')


def remove(request, x):
    user = User.objects.get(id=request.session['id'])
    product = Product.objects.get(id=x)
    user.wishitems.remove(product)
    
    return redirect('/dashboard')

def delete(request, x):
    Product.objects.get(id=x).delete()
    return redirect('/dashboard') 
