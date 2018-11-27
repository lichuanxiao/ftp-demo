import os, sys, json
import hashlib


def secret_key(password_byte):
    hash = hashlib.md5()
    hash.update(password_byte)
    return hash.hexdigest()


def write_userlist(userinfo):
    if not os.path.isfile(r"../conf/userlist"):
        with open(r"../conf/userlist", "w", encoding="utf-8") as f:
            print(userinfo)
            f.writelines(':'.join(userinfo))
    else:
        with open(r"../conf/userlist", "a", encoding="utf-8") as f:
            print(userinfo)
            f.write('\n')
            f.writelines(':'.join(userinfo))


def create_user():
    username = str(input("username:").strip())
    password = str(input("password:").strip())
    passwd_hash = hashlib.md5()
    passwd_hash.update(password.encode("utf-8"))
    userinfo = (username, secret_key(passwd_hash.hexdigest().encode("utf-8")))
    write_userlist(userinfo)


def get_user(username):
    with open(r"../conf/userlist", "r", encoding="utf-8") as f:
        for line in f.readlines():
            print(line)
            print(username)
            print(line.split(":")[0])
            if line.split(":")[0] == username:
                return line.split(":")
        return


def auth(username, password, default_dir='root_dir'):
    password_final_id = secret_key(password.encode("utf-8"))
    userinfo = get_user(username)

    if userinfo and userinfo[1] == password_final_id:
        return True
    else:
        return False

if __name__ =="__main__":
    create_user()