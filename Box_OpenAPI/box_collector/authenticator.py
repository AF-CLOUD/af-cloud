"""
============================================
    "authenticator" Module
============================================
.. moduleauthor:: Seung Ah Kang <kyn0503121@korea.ac.kr>
.. note::
    'TITLE'             : Box - Authenticator in AF-Forensics\n
    'AUTHOR'            : Seung Ah Kang\n
    'TEAM'              : DFRC\n
    'VERSION'           : 0.0.1\n
    'RELEASE-DATE'      : 
--------------------------------------------
Description
===========

    Box Open APIs 를 사용하기 위해 필요한 인증정보 (Oauth Token) 수집하는 모듈
    도구이름    : Forensics Acquisition & Criminal investigation Tool(FACT)\n
    프로젝트    : 안티-포렌식 기술 대응을 위한 데이터 획득 및 분석 기술 연구\n
    연구기관    : 고려대학교(Korea Univ.)\n
    지원기관    : 경찰청, 과학기술정보통신부
"""

from auth import authenticate
from boxsdk import OAuth2
import os
import bottle
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from boxsdk import OAuth2
from boxsdk import Client
from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole




class Authentication:
    def __init__(self, credential):
        self.__id = credential[0]
        self.__password = credential[1]
        self.__authdata =None

    def login (self):
        print("auth")
        oauth, _, _ = authenticate()
        self.__authdata = Client(oauth)

    def run(self):
        print("로그인을 시작합니다. ")
        self.login()
        return self.__authdata