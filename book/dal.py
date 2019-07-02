from models import *


def get_topic(query):
    """
    """
    try:
        obj = Topic.objects.get(query)
    except:
        return None
    return obj


def get_course(query):
    """
    """
    try:
        obj = Course.objects.get(query)
    except:
        return None
    return obj


def filter_course(query):
    """
    """
    try:
        objs = Course.objects.filter(query)
    except:
        return None
    return objs


def filter_topic(query):
    """
    """
    try:
        objs = Topic.objects.filter(query)
    except:
        return None
    return objs
