from django.conf.urls import url
from . import views

app_name = 'questions'

urlpatterns = [
    # /comp/question
    url(r'^question/(?P<user_id>[0-9]+)/$', views.generate, name='generate'),
    # /comp/next_question/[question_id]
    url(r'^next_question/(?P<user_id>[0-9]+)/$', views.next, name='next'),
    # /comp/login
    url(r'^register/$', views.register, name='register'),
    # /comp/login/check_login
    url(r'^login/check_login/$', views.check_login, name='check_login'),
    # /comp/print_all_questions
    url(r'^print_all_questions/$',views.print_all_questions,name = 'print_all_questions'),
    # /comp/leaderboard/[user_id]
    url(r'^leaderboard/(?P<user_id>[0-9]+)/$', views.leaderboard, name='leaderboard'),
    url(r'^instruction_view/(?P<user_id>[0-9]+)/$', views.instruction_view, name='instruction_view'),

    url(r'^update/$', views.update_leaderboard, name='update_leaderboard')



]
