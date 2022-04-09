#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings 
from datetime import datetime
from django.conf import settings
import zipfile
from os import walk
import shutil
import os
import json

# Create your models here.\

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(deletedAt__isnull=True)

class BaseModel(models.Model):

    """
    Base model
    """
    objects = BaseModelManager()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null = True)

    def soft_delete(self, *args, **kwargs):
        self.deletedAt = datetime.now()
        self.save()

    def delete(self):
        self.soft_delete()

    class Meta:
        """
        Class meta
        """
        abstract = True


class Document(BaseModel):
    docfile = models.FileField(default = None, verbose_name='Content Image')
    video_name  = models.ForeignKey(Video, default = None, on_delete=models.PROTECT) #default hoosnoor ugwul shalgah vyd aldaa garah magadlalatai
    subject_number = models.CharField(max_length=100,default= None)
    chatbot_port = models.CharField(max_length=100,default=None,unique=True)
    chatbot_ip = models.CharField(max_length=100,default=None,unique=True)
    chatbot_name = models.CharField(max_length=500,default=None, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if self.docfile:
            tmp_DocFile = self.docfile
            tmp_video_name = self.video_name
            tmp_cbot_name = self.chatbot_name
            tmp_s_number = self.subject_number
            self.docfile = None
            isUpdate = False

            if (self.id):
                isUpdate = True
                old_model = Document.objects.values().get(id = self.id)
                
            # creating image path with id
            super(Document, self).save(*args, **kwargs)
            if not isUpdate:
                old_model = False
            self.docfile = tmp_DocFile

            dir_path = '/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/zip_files/'
            full_dir_path = dir_path + str(tmp_DocFile)
            if not isUpdate or (isUpdate and tmp_DocFile.name != old_model['.zip'] or tmp_DocFile.name != old_model['.py'] or tmp_DocFile.name != old_model['.json']):
                self.docfile.name = full_dir_path
                self.dir_path = dir_path
                self.url = full_dir_path

        super(Document, self).save(*args, **kwargs)

    def get_dict(self):
        data = dict()
        data['docfile'] = str(self.docfile)
        data['video_name'] = str(self.video_name)
        data['subject_number'] = str(self.subject_number)
        data['chatbot_name'] = str(self.chatbot_name)
        data['chatbot_port'] = str(self.chatbot_port)
        data['chatbot_ip'] = str(self.chatbot_ip)
        if True:
            with zipfile.ZipFile(data['docfile'], 'r') as tmp:           
                    tmp.extractall('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/')
            chatbots_loc = '/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/'
            csv_file_loc = '/home/eilab/tt_moocatalk/homepage/D-chatbots/data/'
            filenames = os.listdir(chatbots_loc)
            for filename in filenames:
                full_filename = os.path.join(chatbots_loc, filename)
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.csv': 
                    print(full_filename)
                    print(filename)
                    shutil.move(chatbots_loc+filename,csv_file_loc+filename)
            chatbot_name_ = str(self.chatbot_name)
            chatbot_port_ = str(self.chatbot_port)
            chatbot_ip_ = str(self.chatbot_ip)
            pathd = os.path.isfile('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json')
            if pathd:
                print("pathd---------------->",pathd)
                with open('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json','r') as read_chatbot_port:
                    read_port = json.load(read_chatbot_port)
                with open('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json','w') as chatbot_port1:
                    if chatbot_port_ not in read_port.values():
                        read_port[chatbot_name_] = [chatbot_ip_,chatbot_port_]
                        json.dump(read_port,chatbot_port1)
                    else:
                        json.dump(read_port,chatbot_port1)
            else:
                with open('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json','w') as dump_chatbot_port:
                    json.dump({},dump_chatbot_port)
                with open('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json','r') as read_chatbot_port:
                    read_port = json.load(read_chatbot_port)
                with open('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json','w') as chatbot_portd:
                    if chatbot_port_ not in read_port.values():
                        read_port[chatbot_name_] = [chatbot_ip_,chatbot_port_]
                        json.dump(read_port,chatbot_portd)
                    else:
                        json.dump(read_port,chatbot_portd)
        return data


