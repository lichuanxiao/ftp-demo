__all__ = ["register", "login"]

import hashlib
from conf import settings
from core.user import User
import json
import os


def __secret(passwd_md5):
    secret_key = "jst-ftp"
    passwd_f = hashlib.md5()
    passwd_f.update((passwd_md5+secret_key).encode(settings.CODE))
    return passwd_f.hexdigest()


def __get_userinfo(username):
    with open("../db/passwd","r") as f:
        for line in f.readlines():
            if line.split(":")[0] == username:
                print(line)
                return line.split(":")
    return False


def register(**kwarg):
    if __get_userinfo(kwarg["username"]):
        print("用户已存在")
        return (False,"用户已存在")
    passwd_f_md5 =  __secret(kwarg["password"])
    user_obj = User(kwarg["username"],0)
    userinfo = ":".join([user_obj.username,passwd_f_md5,user_obj.db_path])
    with open("../db/passwd","a") as f:
        f.write("\n")
        f.write(userinfo)
    if not os.path.exists(user_obj.homepath):
        os.mkdir(user_obj.homepath)
    user_obj.dumpinfo()
    return (True,"用户注册成功",user_obj)


def login(**kwarg):
    userinfo = __get_userinfo(kwarg["username"])
    if not userinfo:
        return (False,"用户不存在")
    if userinfo[1] == __secret(kwarg["password"]):
        user_obj = User.loadinfo(kwarg["username"])
        return (True,"登陆成功",user_obj)
    else:
        return (False,"密码错误")
