import json
import os
import socket
import dialogflow_v2 as dialogflow
from flask import Flask,request,jsonify
from _thread import *

import argparse
import uuid
#cloudbot1-heyr-a31c56e3de84.json
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=' '

from google.protobuf.json_format import MessageToJson
b = list()
ServerSideSocket = socket.socket()
host = ' '
port = 
ThreadCount = 0
language = 'ko'
try:
    ServerSideSocket.bind((host,port))
except socket.error as e:
    print(str(e))
print('Socket is listening.. {}'.format(ServerSideSocket.getsockname()))
ServerSideSocket.listen(5)
def multi_threaded_client(connection):

    connection.send(str.encode('Server is working:'))

    while True:
        text = connection.recv(2048)
        language_code = 'ko'
        print('text----------->',text)
        """Returns the result of detect intent with texts as inputs.
        Using the same `session_id` between requests allows continuation
        of the conversation."""
        project_id=" "
        # project_id="dorj-dialogflow-ccmt"
        session_id="session01"
        #session_id="projects/acquired-ripple-285306/agent/sessions/22976af6-873e-2f74-ac90-bdbbcfbe6815"
        language_code=language
        
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        intentdict={'definition':"정의", 'cons':"단점",'contrast':"차이점",'example':"예시",'pros':"장점",'feature':"특징",'Default Fallback Intent':"기타"}
        print('Session path: {}\n'.format(session))
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        print('query_input-----------<',query_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        
        res=MessageToJson(response)
        res=json.loads(res)
        print(res)
        intent=res['queryResult']['intent']['displayName']
        ins = res['queryResult']['fulfillmentText']
        b.append(ins)
        with open('ports/chatbot_db_port.json','r') as read_port:
            uploaded_ports = json.load(read_port)
        for name, port_val in uploaded_ports.items():
            for val in port_val:
                if '.' in val:
                    ip = val
                else:
                    port_ = val
            if port == int(port_) and host == ip:
                uploaded_name = name
        with open('../../../broker/codes/save_port.json','r') as infile:
            df = json.load(infile)
            for key, value in df.items():
                if port == value:
                    my_name_ = key
        for i in b:
            d = my_name_+'번 챗봇 '+uploaded_name+': '+i
        connection.sendall(str.encode(d))
        connection.close()
        
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()

