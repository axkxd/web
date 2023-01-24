from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.new_questions, name = 'main'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^logout/$', views.user_logout, name = 'logout'),
    url(r'^signup/$', views.user_signup, name = 'signup'),
    url(r'^question/(?P<id>\d+)/$', views.question_details, name = 'question'),
    url(r'^ask/$', views.ask_question, name = 'ask'),
    url(r'^popular/$', views.popular_questions, name = 'popular'),
    url(r'^new/$', views.new_questions, name = 'new'),
]