from django.conf.urls import url

from . import views
import account

urlpatterns = [
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^ranking/$', views.question_ranking, name='ranking'),
    url(r'^question/$', views.question, name='question'),
    url(r'^question/(?P<id>\d+)/$', views.question_detail, name='question_detail'),
    url(r'^topic/$', views.topic, name='topic'),
    url(r'^people/edit/$', account.views.profile_edit, name='profile_edit'),
    url(r'^people/follow/$', views.user_follow, name='user_follow'),
    url(r'^people/(?P<username>[-\w]+)/$', views.people, name='people'),
    url(r'^question/(?P<id>\d+)/answer/create/$', views.create_answer, name='create_answer')
]