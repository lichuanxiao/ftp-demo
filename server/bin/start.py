import sys,os
import socketserver
sys.path.append(os.path.dirname(os.getcwd()))
from core.server import MyFTPserver

IP = "127.0.0.1"
PORT = 8099

if __name__ == "__main__":
    socket_obj = socketserver.ThreadingTCPServer((IP,PORT),MyFTPserver)
    socket_obj.serve_forever()
