import socketserver
import os, sys, json
from user import auth, create_user


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        userinfo_bytes = self.request.recv(1024)
        userinfo = json.loads(userinfo_bytes.decode("utf-8"))
        print(userinfo)
        if auth(**userinfo):
            self.request.send('连接成功'.encode("utf-8"))
        else:
            self.request.send('连接失败'.encode("utf-8"))


if __name__ == "__main__":
    mysocket = socketserver.ThreadingTCPServer(('127.0.0.1',9999),Myserver)
    if not os.path.isfile(r"../conf/userlist"):
        print("文件不存在,请创建用户")
        create_user()
    mysocket.serve_forever()
