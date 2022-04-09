from django.contrib import admin
from django.urls import  include, path, re_path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'moocacha'
urlpatterns = [
    path('chatbot',views.documentSave),
]
