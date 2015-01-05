__author__ = 'micanzhang'

import os
import sys
import shutil
import ctypes


def win32_setup():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        exit("permission denies, you should run as administrator")

    cur_dir = os.getcwd()
    cmd = "python " + cur_dir + '\\run.py %*'
    f = open("hosts.bat", 'w')
    f.write("@echo off\n")
    f.write(cmd)
    f.close()

    usr_bin = 'D:\\Applications'
    if not os.path.exists(usr_bin):
        os.mkdir(usr_bin)
    shutil.copyfile("hosts.bat", usr_bin + "\\hosts.bat")

    env_path = os.environ['path']
    if env_path.find(usr_bin) == -1:
        cmd = "SETX PATH \"%PATH%;" + usr_bin + "\" /M"
        os.system(cmd)



def posix_setup():
    pass


if __name__ == "__main__":
    if sys.platform == 'win32':
        win32_setup()
    else:
        posix_setup()


