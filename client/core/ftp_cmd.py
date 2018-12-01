import os
import struct
import json

cmd_list = [("上传", "upload"), ("下载", "download"), ("创建目录", "mkdir"),
            ("删除目录", "deldir"), ("上级目录", "parentdir"),
            ("切换目录", "changedir"), ("删除文件", "delfile"),
            ("退出", "quit"), ("查看当前目录", "ls"), ("用户信息", "showme")]


class Cmd():
    def __init__(self,auth_obj_socket):
        self.socket = auth_obj_socket
        self.cmd_list = cmd_list

    def sendhead(self,head):
        head_bytes = json.dumps(head).encode("utf-8")
        head_len_bytes = struct.pack("i", len(head_bytes))
        self.socket.sk.send(head_len_bytes)
        self.socket.sk.send(head_bytes)

    def upload(self):
        upload_file_path = input("请输入你要上传的文件路径:").strip()
        if not os.path.isfile(upload_file_path):
            print("找不到该文件")
        file_size = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)
        head = {"file_size":file_size,"file_name":file_name,"cmd":"upload"}
        self.sendhead(head)
        with open(upload_file_path,'rb') as f:
            while 1:
                block = f.read(1024)
                if not block:
                    break
                self.socket.sk.send(block)
                #TODO:添加 md5 对比
