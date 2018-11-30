from conf import settings
import os
import pickle
root_path = os.path.dirname(os.getcwd())

class User():
    def __init__(self,username,diskspace,used_space=0):
        self.__username = username
        self.__diskspace = diskspace
        self.__currentpath = self.homepath
        self.__used_space = used_space
    @property
    def username(self):
        return self.__username

    @property
    def homepath(self):
        return os.path.join(settings.ROOTPATH,self.__username)
    @property
    def db_path(self):
        return os.path.join(root_path,"db","user",self.__username)
    @property
    def diskspace(self):
        return self.__diskspace

    @property
    def currentpath(self):
        return self.__currentpath
    @currentpath.setter
    def currentpath(self,value):
        pass

    @property
    def used_space(self):
        return self.__used_space 
    @used_space.setter
    def used_space(self):
        pass
    def func_list(self):
        return ["upload","download","mkdir","change_dir","show_me","ls",'"quit"]
    def dumpinfo(self):
        info = {"username":self.username,"diskspace":self.diskspace,"used_space":self.used_space}
        with open(self.db_path,'wb') as f:
            pickle.dump(info,f)

    @staticmethod
    def loadinfo(username):
        db_path = os.path.join(root_path,"db","user",username)
        with open(db_path,'rb') as f:
            info = pickle.load(f)
            return User(**info)
