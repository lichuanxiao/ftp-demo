import socket
import json
import hashlib
IP = "127.0.0.1"
PORT = 8099
CODE = "utf-8"

class Mysocket():
    def __init__(self):
        self.sk = socket.socket()
        self.sk.connect((IP,PORT))
    def mysend(self,userinfo):
        self.sk.send(json.dumps(userinfo).encode(CODE))


class Auth():
    __instance = False
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            obj = object.__new__(cls)
            obj.socket = Mysocket()
            obj.username = None
            cls.__instance = obj
        return cls.__instance


    def register(self):
        username = input("username:>>>").strip()
        password = input("password:>>>").strip()
        password_ensure = input("password_ensure:>>>").strip()
        if username and password and password == password_ensure:
            passwd_md5 = self.md5_passwd(password)
            self.socket.mysend({"username":username,"password":passwd_md5,"operation":"register"})


    def login(self):
        username = input("username:>>>").strip()
        password = input("password:>>>").strip()
        if username and password:
            passwd_md5 = self.md5_passwd(password)
            self.socket.mysend({"username":username,"password":passwd_md5,"operation":"login"})
    
    
    def md5_passwd(self,password):
        hash_pw = hashlib.md5()
        hash_pw.update(password.encode(CODE))
        return hash_pw.hexdigest()
  
