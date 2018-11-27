import socket
import hashlib
import json


def auth():
    USERINFO = {}
    username = input("请输入用户名：")
    password = input("请输入密码:")
    hash = hashlib.md5()
    hash.update(password.encode("utf-8"))
    USERINFO["username"] = username
    USERINFO["password"] = hash.hexdigest()
    print(USERINFO)
    return USERINFO


if __name__ == "__main__":
    ADDR = '127.0.0.1'
    PORT = 9999
    ADDRESS = (ADDR, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(ADDRESS)
    userinfo = auth()
    sk.send(json.dumps(userinfo).encode("utf-8"))
    responce = sk.recv(1024)
    print (responce.decode("utf-8"))
    sk.close()