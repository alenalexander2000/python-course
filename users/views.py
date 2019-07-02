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

from hashlib import sha512
from uuid import uuid4

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
    request.session['username'] = user.user.first_name

    return redirect('/')


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
    name = data.get('username')
    mobile = data.get('mobile')
    email = data.get('email')
    password = data.get('password')

    user_dict = {
        'name':name,
        'mobile': mobile,
        'email': email,
        'password': password,
    }
    user = create_custom_user(user_dict)
    request.session['accesstoken'] = user.access_token
    request.session['username'] = user.user.first_name

    return redirect('/')


def create_custom_user(user_dict):
    """
    Function to create Custom user object.

    Input Params:
        user_dict(dict): Collection obj with,
            user(obj): django user.
    Returns:
         (obj): User object
    """
    user_dict['user'] = create_djago_user(user_dict)
    user_dict['access_token'] = _generate_key(90)
    user = CustomUser.objects.create(
        user=user_dict['user'],
        access_token=user_dict['access_token'],
        phone=user_dict['mobile']
    )
    return (user)


def create_djago_user(user_dict):
    """
    Function to create Django user.

    Input Params:
        user_dict(dict): Collection obj with,
            name (char): First name of the user
            email (char): valid email id of the user
            password (char): password of the user
    Returns:
        (obj): User object
    """
    user_dict['username'] = user_dict['email'].lower()
    user = User.objects.create_user(
        user_dict['username'],
        user_dict['email'],
        user_dict['password'])
    user.first_name = user_dict['name']
    user.save()
    user.set_password(user_dict['password'])
    user.save()
    return (user)


def _generate_key(length):
    """
    Function to generate a key.

    the following parameters is to be passed.
    :param str length: length of key
    """
    return sha512(uuid4().hex).hexdigest()[:length]
