import socketserver
import json
from core import view
from conf import settings
import struct


class MyFTPserver(socketserver.BaseRequestHandler):

    def recv_head(self):
        head_len = struct.unpack("i", self.request.recv(4))
        head_json_obj = self.request.recv(head_len[0]).decode(settings.CODE)
        return json.loads(head_json_obj)

    def ftp_cmd(self, user_obj):
        while 1:
            ftp_head = self.recv_head()
            print(ftp_head)
            ftp_cmd_str = ftp_head["cmd"]
            if hasattr(user_obj, ftp_cmd_str):
                ftp_cmd_final = getattr(user_obj,ftp_cmd_str)
                cmd_return = ftp_cmd_final(self.request,**ftp_head)
                print(cmd_return)
            else:
                print("错误的操作码!")

    def handle(self):
        try_num = 3
        while 1:
            try_num -= 1
            message_bytes = self.request.recv(1024)
            print(message_bytes)
            message = json.loads(message_bytes.decode(settings.CODE))
            print(message)
            ope_obj = message["operation"]
            if hasattr(view, ope_obj):
                operation = getattr(view, ope_obj)
                ret = operation(**message)
                print(ret)
                print("发送完成")
                if ret[0]:
                    user_obj = ret[2]
                    response = {"status":ret[0],"message":ret[1],"func_list":ret[2].func_list()}
                    self.request.send(json.dumps(response).encode(settings.CODE))
                    self.ftp_cmd(user_obj)
                
                self.request.send(json.dumps({"status":ret[0],"message":ret[1],"func_list":None}).encode(settings.CODE))
            else:
                print("错误的操作码!")
            if not try_num:
                print("尝试次数三次,自动退出。")
                exit()



