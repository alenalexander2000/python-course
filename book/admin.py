# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Completion)
admin.site.register(TopicCompletion)
admin.site.register(Suppliment)
