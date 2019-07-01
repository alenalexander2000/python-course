# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from json import dumps, loads
from datetime import datetime
from uuid import uuid4
from base64 import b64decode
import json
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.validators import validate_email
from django.core.files import File

from django.views import generic
# from .models import Product,User,Batch,Purchase,Plist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
# from .forms import UserForms
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.contrib import messages

from .models import *
from django.contrib.auth import authenticate

# Create your views here.
def signup_page(request):
    """
    """
    messages.info(request, 'Your password has been changed successfully!')
    return render(request, 'signup.html', {'messages' : 'you are an asshole'  })


def signin_page(request):
    """
    """
    return render(request, 'signin.html', {'message' : ''  })


def loginprocess(request):
    data = request.POST
    user_dict ={}
    user_dict['username'] = data.get('email')
    user_dict['password'] = data.get('password')
    user_dict['request'] = request
    user = verify_user_credentials(user_dict)
    request.session['accesstoken'] = user.access_token

    return render(request, 'home.html', {'message' : ''  })


def verify_user_credentials(user_dict):
    """
    Function to validate user credentials and access.

    Input_params:
        user_dict(dict): Collection object, which has the
            following parameters,
            username (char): user name of the user.
            password (char): password of the user.
    Returns:
        user(obj): user object.
    """
    user = authenticate(
        username=user_dict['username'], password=user_dict['password'])

    # try:
    user = CustomUser.objects.get(user=user)
    # except:
    #     return render(user_dict['request'], 'error.html', {'message' : 'Querry error'  })
    #
    # if user.blocked:
    #     return render(user_dict['request'], 'error.html', {'message' : 'Querry error'  })
    return user


def signupprocess(request):
    data = request.POST
    name = data.get('name')
    phone = data.get('mobile')
    phone = data.get('email')
    phone = data.get('password')

    val=1
    batch = Batch.objects.all()
    for i in batch:
        if(i.cbid == cbid): val=0;break
    dict = {'name' : name , 'batch': batch , 'phonenumber' : cbid,'cbid' : phone,'adm_no' : adm_no, 'message' : 'Error'}
    if(password == '' or  password.__len__() >= 100 or password.__len__() <= 7):
        dict['signupmessage'] = "Enter a valid password ** It should contain more than 7 charecters ** "
        return render(request,'list/login.html',dict)
    elif(name == ''):
        dict['signupmessage'] = "Enter a valid name"
        return render(request,'list/login.html',dict)
    elif(adm_no == '' ):
        dict['signupmessage'] = "Enter a valid admission number"
        return render(request,'list/login.html',dict)
    elif(val==1):
        dict['signupmessage']="enter a valid course/class"
    '''try:
        phone = int(phone)
    except Exception, e:
        dict['signupmessage'] = "Enter a valid phone number"
        return render(request,'list/login.html',dict)'''
    data = User.objects.all()
    email_check = User.objects.all().filter(adm_no = adm_no)
    for y in email_check :
        dict['signupmessage'] = "This adm_no is already in use . Please try again with another adm_no "
        return render(request,'list/login.html',dict)
    request.session['logid'] = adm_no


    p = User(name = name,password=password,adm_no=adm_no,phone_no =phone,cbid=i)
    p.save()
    return render(request, 'list/login.html' , {'message' : " Signup Completed Please check Email and Login to continue "})
