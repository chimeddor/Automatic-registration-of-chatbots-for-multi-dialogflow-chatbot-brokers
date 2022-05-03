import re
import socketserver
import socket
import threading
import json
import random
import os
import csv
import socket
from django.db import models
from konlpy.tag import Okt
class Chatbot():
    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            # message parsing
            message = self.rfile.readline().strip()
            message = message.decode("utf-8")
            print("msg:"+message)
            message = json.loads(message)
            data = {}
            data['contents'] = message
            lis = list()
            with open('/home/eilab/tt_moocatalk/homepage/D-chatbots/chatbots/ports/chatbot_db_port.json','r') as read_port:
                uploaded_ports = json.load(read_port)
                for name, key in uploaded_ports.items():
                    lis.append(key)
                choice = random.choice(lis)
                for ip in choice:
                    if '.' in ip:
                        hosts = ip
                    else:
                        ports = ip
            ClientMultiSocket = socket.socket()
            host = hosts
            port = int(ports)
            print('Waiting for connection response')
            check_path = os.path.isfile('save_port.json')
            if check_path:
                with open('save_port.json','r') as infile1:
                    d = json.load(infile1)
            else:
                with open('save_port.json','w') as wri_file:
                    json.dump({},wri_file)
                with open('save_port.json','r') as infile:
                    d = json.load(infile)
            d = d
            try:
                ClientMultiSocket.connect((host, port))
                host, port = ClientMultiSocket.getpeername()
                with open('save_port.json', 'w') as outfile:
                    if port not in d.values():
                        if len(d) == 0:
                            d[1] = port
                            json.dump(d,outfile)
                        else:
                            d[len(d)+1] = port
                            json.dump(d,outfile)
                    else:
                        json.dump(d,outfile)
                    outfile.close()
                print('나랑 연결된 포드는: ',d.values())
            except socket.error as e:
                print(str(e))
            res = ClientMultiSocket.recv(1024)
            if True:
                Input = data["contents"]
                test = ClientMultiSocket.send(str.encode(Input))
                res = ClientMultiSocket.recv(1024)
                # host, port = ClientMultiSocket.getpeername()
                response = res.decode('utf-8')
                print('message: ', response)
            #서버에서 온 메시지를 카카로 보내줌
            answer = response
            ClientMultiSocket.close()
            
