from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('getpage',views.getpage, name='getpage'),
    path('History',views.History,name='history')
]