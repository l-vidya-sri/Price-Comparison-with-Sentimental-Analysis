import functools
import operator
from django.db.models import Q


import mimetypes
import os
import pickle

from django.shortcuts import render
from django.http import HttpResponse, request
from .models import *

import matplotlib.pyplot as plt;
import numpy as np
import numpy
from django.shortcuts import render, redirect

from .DateTime import getdate


def homepage(request):
    #priceupdate()
    return render(request, 'index.html')

def signuppage(request):
    if request.method == 'POST':
        email = request.POST['email']

        d = users.objects.filter(email__exact=email).count()
        if d > 0:
            return render(request, 'signup.html', {'msg': "Email Already Registered"})

        else:

            password = request.POST['password']
            phone = request.POST['phone']
            name = request.POST['name']

            
            d = users(name=name, email=email, password=password, phone=phone)
            d.save()


            return render(request, 'signup.html', {'msg': "Register Success, You can Login.."})

    else:

        return render(request, 'signup.html')


def userloginaction(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        pass_word = request.POST['pwd']
        if uid == 'admin' and pass_word == 'admin':
            request.session['adminid'] = 'admin'
            return render(request, 'admin_home.html')
        else:
    
            d = users.objects.filter(email__exact=uid).filter(password__exact=pass_word).count()
    
            if d > 0:
                d = users.objects.filter(email__exact=uid)
                request.session['email'] = uid
                request.session['name'] = d[0].name
                dat_e=getdate()

                p=notifications.objects.filter(email=uid).filter(dat_e=dat_e).count()
                if p>0:
                    pass
                else:
                    pricealertupdate(uid)
                return render(request, 'user_home.html', {'data': d[0]})
            else:
                return render(request, 'index.html', {'msg': "Login Fail"})

    else:
        return render(request, 'user.html')



def adminhomedef(request):
    if "adminid" in request.session:
        uid = request.session["adminid"]
        return render(request, 'admin_home.html')

    else:
        return render(request, 'admin.html')

def adminlogoutdef(request):
    try:
        del request.session['adminid']
    except:
        pass
    return render(request, 'index.html')



def userlogoutdef(request):
    email= request.session["email"]
    del request.session['email']
    return render(request, 'index.html')


def userhomedef(request):
	if "email" in request.session:
		email=request.session["email"]
		d=users.objects.filter(email__exact=email)
	
		return render(request, 'user_home.html',{'data': d[0]})

	else:
		return redirect('n_userlogout')




def datasetupload(request):
    if request.method == 'POST':
        file = request.POST['file']
        import xlrd
        from .WebCrawl import get_price
        from .RandomGen import getnum
        from .DateTime import getdate
        dat_e=getdate()
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_index(0)
        #return prod_name, description, img, cnames, prices
        for r in range(1, sheet.nrows):
            url = sheet.cell(r, 0).value
            cat = sheet.cell(r, 1).value
            url=url.strip()
            c=products.objects.filter(URL=url).count()
            if c>0:
                pass
                
            else:
                data=get_price(url)
                name=data[0]
                des=data[1]
                img=data[2]
                cnames=data[3]
                price_data=data[4]

                pid=getnum()
                d=products(pid=pid, URL=url, Category=cat, name=name, img=img, description=des)
                d.save()

                for n in range(len(cnames)):
                    d=prices(pid=pid, price=price_data[n], company=cnames[n], dat_e=dat_e)
                    d.save()
                
        return render(request, 'dataset.html', {'msg':'Dataset uploaded and data crawled !!'})
      
    else:
        
            
        return render(request, 'dataset.html')



def viewdataset(request):
    if "adminid" in request.session:
        d = products.objects.all()
        

        return render(request, 'viewdataset.html', {'data': d})

    else:
        return render(request, 'admin.html')


def viewprice(request, op):
    if "adminid" in request.session:
        dat_e=getdate()
        print('???????????????')
       
        pid=op
        
        d1 = prices.objects.filter(pid=pid).filter(dat_e=dat_e)
        d2 = products.objects.all()

        return render(request, 'viewdataset.html', {'pdata': d1,'data': d2, 'id': pid})

    else:
        return render(request, 'admin.html')


def priceupdate():
    from .WebCrawl import get_price
        
    from .DateTime import getdate
    dat_e=getdate()

    c1=prices.objects.filter(dat_e=dat_e).count()
    if c1>0:
        pass
    else:
        d=products.objects.all()
        for d1 in d:
            url=d1.URL
            data=get_price(url)
            cnames=data[3]
            price_data=data[4]
            for n in range(len(cnames)):
                d2=prices(pid=d1.pid, price=price_data[n], company=cnames[n], dat_e=dat_e)
                d2.save()    

def viewproducts(request):
    d = products.objects.all()

    s=set({})

    for d1 in d:
        s.add(d1.Category)
    s=list(s)


    return render(request, 'products.html', {'data':d, 'cat':s})
    
def viewcatprods(request):
    cid=request.GET['cid']
    d = products.objects.all()
    
    s=set({})
    for d1 in d:
        s.add(d1.Category)
    s=list(s)
    d = products.objects.filter(Category=cid)
    
    return render(request, 'products.html', {'data':d, 'cat':s})


def viewproduct(request):
    pid=request.GET['pid']
    d=products.objects.filter(pid=pid)
    cat=d[0].Category
    
    d2=products.objects.filter(Category=cat).exclude(pid=pid)[:5]

    dat_e=getdate()

    
    p=prices.objects.filter(pid=pid).filter(dat_e=dat_e)
    
    return render(request, 'viewproduct.html', {'data':d,'data2':d2, 'prices':p})



def viewreviews(request):
    pid = request.GET['pid']
    d=reviews.objects.filter(pid=pid)
    p=0;n=0;ne=0;
    for d1 in d:
        if d1.sentiment=='Positive':
            p=p+1
        elif d1.sentiment=='Negative':
            n=n+1
        else:
            ne=ne+1
    
        

    return render(request, 'feedback.html', {'data':d, 'p':p, 'n':n, 'ne':ne})


def postreviewpage(request):
    pid = request.GET['pid']
    return render(request, 'postreview.html', {'pid':pid})

def postreview(request):

    review = request.GET['review']
    rating = request.GET['rating']
    pid = request.GET['pid']
    email=request.session['email']
    name=request.session['name']
    print(review, rating, pid, email, name, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,,')

    from .SentimentDetection import analyze_sentiment
    sentiment=analyze_sentiment(review)
    

    p=reviews(pid=pid, review=review, rating=rating, email=email, name=name, sentiment=sentiment)
    p.save()

    d=products.objects.filter(pid=pid)
    dat_e=getdate()
    
    p=prices.objects.filter(pid=pid).filter(dat_e=dat_e)
    
    return render(request, 'postreview.html', { 'pid':pid,'msg':'Review Posted Successfully !!'})



def pricehistory(request):
    pid=request.GET['pid']
    dates=[]
    services=set({})

    d=prices.objects.filter(pid=pid).order_by('dat_e')
    for d1 in d:
        if d1.dat_e in dates:pass
        else:dates.append(d1.dat_e)
        services.add(d1.company)
    
    l={}
    
    for s1 in services:
        l1=[]

        for d1 in dates:
            d=prices.objects.filter(pid=pid).filter(dat_e=d1).filter(company=s1)
            p=d[0].price
            p=p.replace('₹','')
            p=p.replace(',','')
            l1.append(p)
        l[s1]=l1
    print(l)
    """filename = 'history.csv'
    import csv
    
    with open(filename,  'w', newline='') as file:
        writer = csv.writer(file, )
        writer.writerows(l)
    """
    from .LineGraph import generate
    generate(dates, l)
    
    
    d=products.objects.filter(pid=pid)
    dat_e=getdate()
    
    p=prices.objects.filter(pid=pid).filter(dat_e=dat_e)
    
    return render(request, 'viewproduct.html', {'data':d, 'prices':p})


 
def pricealertdef(request):
    pid=request.GET['pid']

    dat_e=getdate()
    
    p=prices.objects.filter(pid=pid).filter(dat_e=dat_e)
    price_s=[]
    for p1 in p:
        cost=p1.price
        cost=cost.replace('₹','')
        cost=cost.replace(',','')
        price_s.append(int(cost))
    
    cost=min(price_s)

    email=request.session["email"]

    d=pricealert(pid=pid, email=email, price=cost)
    d.save()
              
        
    
    
    d=products.objects.filter(pid=pid)
    
    
    return render(request, 'viewproduct.html', {'data':d, 'prices':p, 'msg':'Price Alert Applied for this Item'})


 
def pricealertupdate(email):
    
    dat_e=getdate()
    
    p=pricealert.objects.filter(email=email)
    for p1 in p:
        pcost=p1.price
        pid=p1.pid

        costs=[]

        d=prices.objects.filter(dat_e=dat_e).filter(pid=pid)
        for d1 in d:
            cost=d1.price
    
        
            cost=cost.replace('₹','')
            cost=cost.replace(',','')
            costs.append(int(cost))
    
        cost=min(costs)
        print(cost,pcost,'<<<<<<<<<<<', pid)
        if pcost>cost:
            d=products.objects.filter(pid=pid)
            mesg='Price Drop Alert, \nthe price of '+str(d[0].name)+' is dropped today !! Hurry Up!! '
            d=notifications( email=email, mesg=mesg, dat_e=dat_e, stz='new')
            d.save()
            
              
        
    
    
                    

def notificationsdef(request):
    email=request.session['email']
    d=notifications.objects.filter(email=email)
        

    return render(request, 'notifications.html', {'data':d, })

def searchproducts(request):

    keys=request.POST['search']
    lst=keys.split()
    query = functools.reduce(operator.and_, (Q(name__icontains = item) for item in lst))
    d=products.objects.filter(query)
    
    d2=products.objects.all()

    s=set({})

    for d1 in d2:
        s.add(d1.Category)
    s=list(s)


    return render(request, 'products.html', {'data':d, 'cat':s})
