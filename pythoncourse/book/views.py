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
from .constants import *


from django.contrib.auth import authenticate

from hashlib import sha512
from uuid import uuid4

# Create your views here.

def home(request):
    """
    """
    try:
        if not request.session['accesstoken']:
            return redirect('/users/signin/')
    except:
         return redirect('/users/signin/')

    return render(request, 'home.html')


def topic_list(request, course_id):
    """
    """
    try:
        if not request.session['accesstoken']:
            return redirect('/users/signin/')
    except:
        return redirect('/users/signin/')
    topics = Topic.objects.filter(course__id=course_id).order_by('position')
    return render(request, 'topic_view.html', {'topics': topics})


def course_list(request):
    """
    """

    try:
        if not request.session['accesstoken']:
            return redirect('/users/signin/')
    except:
         return redirect('/users/signin/')
    courses = Course.objects.all()
    return render(request, 'course_view.html', {'courses': courses})


def add_content(request):
    """
    """
    try:
        if not request.session['accesstoken']:
            return redirect('/users/signin/')
    except:
         return redirect('/users/signin/')
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


class TopicCreate (CreateView):
    model = Topic
    fields = ['course', 'name', 'description', 'position', 'image']


class ContentDetail(generic.DetailView):
    model = Content
    template_name = 'detail.html'


class ContentUpdate (UpdateView):
    model = Content
    fields = ['topic', 'content', 'position', 'value']


class TopicUpdate (UpdateView):
    model = Topic
    fields = ['course', 'name', 'description', 'position', 'image']
    success_url = reverse_lazy('index')


class TopicDelete (DeleteView):
    model = Topic
    success_url = reverse_lazy('index')


class ContentDelete (DeleteView):
    model = Content
    success_url = reverse_lazy('index')


def content_list(request, topic_id):
    """
    """
    try:
        if not request.session['accesstoken']:
            return redirect('/users/signin/')
    except:
         return redirect('/users/signin/')
    topic = Topic.objects.get(id=topic_id)
    # import ipdb; ipdb.set_trace()
    contents = Content.objects.filter(topic=topic).order_by('position')
    topics = Topic.objects.filter(course=topic.course).exclude(id=topic_id).order_by('position')
    datas = contents
    return render(request,
    'content_view.html',
    {'contents': contents,
        'topics': topics,
        'current_topic': topic,
        'datas': datas})


def search_view(request):
    """
    """
    keyword = request.POST.get('keyword')

    contents = Content.objects.filter(Q(value__icontains=keyword,
    topic__lock=True)).order_by('topic')
    topics = Topic.objects.filter(Q(name__icontains=keyword,
    lock=True)|
    Q(description__icontains=keyword,
    lock=False)).order_by('course')

    return render(request, 'search_view.html', {
    'contents': contents,
    'topics': topics
    })

# def get_content_as_html(contents):
#     data =''
#     import ipdb; ipdb.set_trace()
#     for content in contents:
#         if int(content.content) ==TEXT:
#             data += get_text_html(content)
#         # elif int(content.content) == CODE:
#         #     data += get_code_html(content)
#         # elif int(content.content) == IMAGE:
#         #     data += get_image_html(content)
#         # elif int(content.content) == POINT:
#         #     data += get_point_html(content)
#         # elif int(content.content) == LINK:
#         #     data += get_link_html(content)
#         # elif int(content.content) == GRAPH:
#         #     data += get_graph_html(content)
#         # elif int(content.content) == TABLE:
#         #     data += get_table_html(content)
#         # elif int(content.content) == VIDEO:
#         #     data += get_video_html(content)
#     return data
#
#
# def get_text_html(content):
#     return('<pre><code>' + content.value +'</code></pre>')
