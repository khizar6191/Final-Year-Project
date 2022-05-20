from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home ,name='home'),
    path('menu/',views.menu,name='menu'),
    path('inbox/', views.inbox,name='inbox'),
    path('sent/', views.sent,name='sent'),
    path('trash/', views.trash,name='trash'),
    path('compose/', views.compose,name='compose'),
    path('login/', views.login,name='login'),
    path('am/',include('login.urls')),

    path('instructions/', views.instructions, name='Instructions'),

    path('sample/',views.sample,name='sample'),
]
