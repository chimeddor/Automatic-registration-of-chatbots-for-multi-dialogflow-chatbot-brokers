#-*- coding:utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.conf import settings
from rest_framework import viewsets
from moockt_web.models import Video,Subject
from moockt_web.serializers import *
from chatbot.models import ChatbotUser
from Moocacha_KakaoTalk.config import GLOBAL_PORT
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from flask import Flask, session, url_for
from decimal import Decimal
from datetime import date
import psycopg2
import json



def documentSave(request):
    a = ''
    data = dict()

    if request.method == 'POST' and request.FILES['docfile']:
        # Vname = video_name.type.CharField()
        print("---->",type(request.POST.get('video_name')), request.POST.get('video_name'))
        sub_num = request.POST.get('subject_number')
        video_id = int(request.POST.get('video_name'))
        chatbot_name = request.POST.get('chatbot_name')
        chatbot_port = request.POST.get('chatbot_port')
        chatbot_ip = request.POST.get('chatbot_ip')
        docfile = request.FILES['docfile']
        # cursor.execute("""INSERT INTO introduction(id, intro1, intro2) VALUES(DEFAULT, %s, %s)""",(id, chatbot_name, docfile))
        # conns.commit()
        document = Document()
        document.docfile = docfile
        document.video_name_id = video_id
        document.chatbot_name = chatbot_name
        document.subject_number = sub_num
        document.chatbot_port = chatbot_port
        document.chatbot_ip = chatbot_ip

        try:
            document.save()
            return_data = document.get_dict()
            a = return_data
            print("ene ni bol:",a)
        except Exception as e:
            a = e
            print("ene sdan bol Exce:", a)
    data['data'] = a
    print('a----------->',type(a))
       
    return render(request,"moocacha/chatbot_upload.html", data)
    # return HttpResponse(json.dumps(data, default=convert), content_type='application/json')

