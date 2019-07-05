from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views
from book import views as b_view

urlpatterns = [

    # exception page
    # url(r'^course/(?P<course_id>\d+)/topics/addprocess/$', views.add_content),

    url(r'^home/', b_view.home ,name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
