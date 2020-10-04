from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', redirect_index),
    path('user/auth/', auth_user, name='auth_user'),
    path('payment/', payment, name='payment'),
    path('bad-payment/', bad_payment, name='bad_payment'),
    path('succes-payment/', succes_payment, name='succes_payment'),
    path('payment-check/', payment_check),
    path('index/', index, name='index'),
    re_path('final/(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', final, name='final'),
    re_path('time-to-start/(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', time_to_start, name='time_to_start'),
    re_path('(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/(?P<id_question>[\w-]+)/$', question, name='question'), 
    re_path('(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', start_olympiad, name='start_olympiad'),
    path('profile/', profile, name='profile'),
    path('documents/', documents, name='documents'),
    path('signout/', signout, name='signout')
]