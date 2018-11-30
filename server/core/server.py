import socketserver
import json
from core import view
from conf import settings
class MyFTPserver(socketserver.BaseRequestHandler):
    def handle(self):
        try_num = 3
        while 1:
            try_num -= 1
            message_bytes =  self.request.recv(1024)
            print(message_bytes)
            message = json.loads(message_bytes.decode(settings.CODE))
            print(message)
            ope_obj = message["operation"]
            if hasattr(view,ope_obj):
                operation = getattr(view,ope_obj)
                ret = operation(**message)
                print(ret)
                print("发送完成")
                if ret[0]:
                    user_obj = ret[2]
                    response = {"status":ret[0],"message":ret[1],"func_list":ret[2].func_list()}
                    self.request.send(json.dumps(response).encode(settings.CODE))
                    break
                
                self.request.send(json.dumps({"status":ret[0],"message":ret[1],"func_list":None}).encode(settings.CODE))
            else:
                print("错误的操作码!")
            if not try_num:
                print("尝试次数三次,自动退出。")
                exit()
