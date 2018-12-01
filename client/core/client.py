from core.auth_client import Auth
from core.ftp_cmd import Cmd
import json


def ftp_cmd(cmd_obj):
    for index, item in enumerate(cmd_obj.cmd_list, 1):
        print(index, item[0])
    while 1:
        cmd_num = int(input(">>>选择操作:").strip())
        print(cmd_num)
        if hasattr(cmd_obj, cmd_obj.cmd_list[cmd_num - 1][1]):
            cmd_final = getattr(cmd_obj, cmd_obj.cmd_list[cmd_num - 1][1])
            cmd_final()
        else:
            print("没有这个命令")


def main():
    auth_obj = None
    operation_l = [("登陆", "login"), ("注册", "register"), ("退出", "quit")]
    for index,item in enumerate(operation_l,1):
        print(index,item[0])
    try_num = 3
    while 1:
        if not try_num:
            print("最多尝试三次")
            exit()
        try_num -= 1
        #判断如果三次则退出
        num = int(input("operation:>>>").strip())
        ope_str = operation_l[num-1][1]
        if hasattr(Auth, ope_str):
            auth_obj = Auth()
            operation = getattr(auth_obj,ope_str)
            operation()
            operation_res = json.loads(auth_obj.socket.sk.recv(1024).decode("utf-8"))
            print(operation_res["message"])
            if operation_res["status"]:
               cmd_obj = Cmd(auth_obj.socket)
               ftp_cmd(cmd_obj)
        elif auth_obj:
            auth_obj.socket.sk.close()
            exit()
        else:
            exit()

