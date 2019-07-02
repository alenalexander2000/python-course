# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from book.models import *


from json import dumps, loads
from datetime import datetime
from uuid import uuid4
from base64 import b64decode
import json
from datetime import timedelta
from django.utils import timezone


from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.validators import validate_email
from django.core.files import File

from django.views import generic
# from .models import Product,User,Batch,Purchase,Plist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
# from .forms import UserForms
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.contrib import messages

from . import dal 


from django.contrib.auth import authenticate

from hashlib import sha512
from uuid import uuid4

# Create your views here.

def home(request):
    """
    """
    try:
        if request.session.key['accesstoken']:
            return render(request, 'home.html')
        else:
            return redirect('/users/signin/')
    except:
         return redirect('/users/signin/')


def topic_list(request, course_id):
    """
    """
    topics = Topic.objects.filter(course__id=course_id).order_by('position')
    return render(request, 'topic_view.html', {'topics': topics})


def course_list(request):
    """
    """
    courses = Course.objects.all()
    return render(request, 'course_view.html', {'courses': courses})


def add_content(request):
    """
    """
    data = request.POST
    con_dict = {
        'topic_id': data.get('topic_id'),
        'type': data.get('type'),
        'value': data.get('value'),
        'position': data.get('position')
    }
    topic = Topic.objects.get(id=con_dict['topic_id'])
    content = Content(
        topic=topic,
        content=con_dict['type'],
        value=con_dict['value'],
        position=con_dict['position']
    )
    content.save()
    return redirect('/course/'+str(topic.course.id)+'/topics/')


class ContentCreate (CreateView):
    model = Content
    fields = ['topic', 'content', 'position', 'value']


class ContentDetail(generic.DetailView):
    model = Content
    template_name = 'detail.html'


class ContentUpdate (UpdateView):
    model = Content
    fields = ['topic', 'content', 'position', 'value']


class ContentDelete (DeleteView):
    model = Content
    success_url = reverse_lazy('index')

