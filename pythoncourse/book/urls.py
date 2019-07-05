from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    # exception page
    # url(r'^course/(?P<course_id>\d+)/topics/addprocess/$', views.add_content),
    url(r'^course/(?P<course_id>\d+)/topics/add/$', views.ContentCreate.as_view()),
    url(r'^content/(?P<pk>\d+)/view/$', views.ContentDetail.as_view(),name= 'content'),
    url(r'^content/(?P<pk>\d+)/update/$', views.ContentUpdate.as_view()),
    url(r'^content/(?P<pk>\d+)/delete/$', views.ContentDelete.as_view()),

    url(r'^topic/add/$', views.TopicCreate.as_view()),
        url(r'^topic/(?P<pk>\d+)/update/$', views.TopicUpdate.as_view()),
        url(r'^topic/(?P<pk>\d+)/delete/$', views.TopicDelete.as_view()),

    url(r'^course/(?P<course_id>\d+)/topics/$', views.topic_list),
    url(r'^course/$', views.course_list),

    url(r'^search/$', views.search_view),

    url(r'^topic/(?P<topic_id>\d+)/view/$',views.content_list),
    # url(r'^', views.home,name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
